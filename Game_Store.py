import datetime
import json

# Diccionario de los juegos que están disponibles
game_disponibles = {
    "nintendo": [
        {"game": "Princess Peach: Showtime!", "genero": "Aventura", "precio": 27990},
        {"game": "Mario vs. Donkey Kong", "genero": "Aventura", "precio": 31990},
        {"game": "Hogwarts Legacy", "genero": "Aventura", "precio": 28990}
    ],
    "PS5": [
        {"game": "METAL SLUG ATTACK RELOADED", "genero": "Acción", "precio": 9990},
        {"game": "Crown Wars", "genero": "Acción", "precio": 36990},
        {"game": "EA SPORTS FC 24 FIFA 24", "genero": "Deporte", "precio": 26990},
        {"game": "TopSpin 2K25", "genero": "Deporte", "precio": 22990},
        {"game": "Rugby 22", "genero": "Deporte", "precio": 32990}
    ],
    "PS4": [
        {"game": "Call of Duty Black Black Ops 6", "genero": "Disparos", "precio": 42990},
        {"game": "Red Dead Redemption + Undead Nightmare", "genero": "Disparos", "precio": 32990}
    ]
}

# Carro para almacenar las ventas
game_venta = []


def registrar_venta():
    nombre_cliente = input("Ingrese el nombre del cliente\n")
    tipo_cliente = input("Ingrese el tipo de cliente (Estudiante Trabajador Socio)\n")
    ventas_cliente = []
    while True:
        tipo_consola = input("Ingrese el tipo de consola (Nintendo PS5 PS4)\n")

        if tipo_consola in game_disponibles:
            print(f"Juegos disponibles para {tipo_consola}:")
            for item, game in enumerate(game_disponibles[tipo_consola], start=1):
                print(f"{item}. {game['game']} - {game['genero']} - ${game['precio']}")
        
            inx_game = int(input("Seleccione el numero del juego\n")) - 1
            if 0 <= inx_game < len(game_disponibles[tipo_consola]):
                game_seleccionado = game_disponibles[tipo_consola][inx_game]
                tipo_game = game_seleccionado["genero"]
                precio = game_seleccionado["precio"]

                descuento = obtener_descuento(tipo_cliente)
                precio_final = round(precio * (1 - descuento), 2)

                # Crear un diccionario con los detalles de la venta
                venta = {
                    "nombre_cliente": nombre_cliente,
                    "tipo_cliente": tipo_cliente,
                    "tipo_consola": tipo_consola,
                    "tipo_game": tipo_game,
                    "nombre_juego": game_seleccionado["game"],
                    "precio": round(precio, 3),
                    "descuento": round(precio * descuento, 3),
                    "precio_final": precio_final
                }

                ventas_cliente.append(venta)
                print("Producto agregado con éxito!")
            else:
                print("Selección de juego no válida.")
        else:
            print("Tipo de consola no válido. Intente de nuevo.")

        otra = input("¿Desea agregar otro juego? (s/n)\n").strip().lower()
        if otra != 's':
            break
    # Calcular los totales después de que el cliente termine de agregar juegos
    total_sin_descuento_final = sum(venta["precio"] for venta in ventas_cliente)
    total_con_descuento_final = sum(venta["precio_final"] for venta in ventas_cliente)
    descuento_total = total_sin_descuento_final - total_con_descuento_final
    fecha_hora = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

    # Agregar la venta completa a la lista de ventas
    game_venta.append({
        "nombre_cliente": nombre_cliente,
        "tipo_cliente": tipo_cliente,
        "ventas": ventas_cliente,
        "total_sin_descuento_final": round(total_sin_descuento_final, 3),
        "descuento_total": round(descuento_total, 3),
        "total_con_descuento_final": round(total_con_descuento_final, 3),
        "fecha_hora": fecha_hora
    })

    print("Venta registrada con éxito!")

def mostrar_ventas():
    for venta in game_venta:
        print(venta)

def buscar_producto_por_clientes():
    nombre_cliente = input("Ingrese el nombre del cliente para buscar sus ventas\n").strip().lower()
    ventas_cliente = [venta for venta in game_venta if venta["nombre_cliente"].lower() == nombre_cliente]
    for venta in ventas_cliente:
        print(venta)

def guardar_ventas_en_archivos():
    with open("ventas.json", "w") as archivo:
        json.dump(game_venta, archivo, indent=4)
    print("Ventas guardadas en ventas.json")

def cargar_ventas_en_archivo():
    # Función para cargar ventas desde un archivo JSON.

    global game_venta
    try:
        with open("ventas.json", "r") as archivo:
            game_venta = json.load(archivo)
        print("Ventas cargadas desde ventas.json")
    except FileNotFoundError:
        print("Lo sentimos, no se encontraron archivos en ventas.json")

def generar_boletas(boleta):
    # Función para generar y mostrar la boleta de una venta específica.

    print("\n--- FACTURA ---")
    print(f"Nombre del cliente: {boleta['nombre_cliente']}")
    print(f"Fecha y Hora: {boleta['fecha_hora']}")
    print(f"Tipo de cliente: {boleta['tipo_cliente'].capitalize()}")

    print("\n--- Detalles de la compra ---")
    for item in boleta["ventas"]:
        print(f"- {item['nombre_juego']} {item['tipo_consola'].upper()}, {item['tipo_game']} - ${item['precio']} - Descuento: ${item['descuento']} - Total: ${item['precio_final']}")
    
    print("\n--- Resumen de Pagos ---")
    print(f"Precio original: ${boleta['total_sin_descuento_final']}")
    print(f"Descuento total: ${boleta['descuento_total']}")
    print(f"Total a pagar: ${boleta['total_con_descuento_final']}")
    print("----------------")

def obtener_descuento(tipo_cliente):
    # Función para obtener el descuento basado en el tipo de cliente.

    if tipo_cliente.lower() == "estudiante":
        return 0.15
    elif tipo_cliente.lower() == "trabajador":
        return 0.10
    elif tipo_cliente.lower() == "socio":
        return 0.20
    else:
        return 0.0

def menu():
    # Función principal que muestra el menú y gestiona la interacción con el usuario.

    while True:
        print("\n--- GAME STORE TOTORO ---")
        print("1. Registrar una venta")
        print("2. Mostrar todas las ventas")
        print("3. Buscar ventas por cliente")
        print("4. Guardar las ventas en un archivo")
        print("5. Cargar las ventas desde un archivo")
        print("6. Imprimir factura")
        print("7. Salir del programa")

        opción = int(input("Seleccione una opción\n"))

        if opción == 1:
            registrar_venta()
        elif opción == 2:
            mostrar_ventas()
        elif opción == 3:
            buscar_producto_por_clientes()
        elif opción == 4:
            guardar_ventas_en_archivos()
        elif opción == 5:
            cargar_ventas_en_archivo()
        elif opción == 6:
            nombre_cliente = input("Ingrese el nombre del cliente para imprimir la factura\n").strip().lower()
            ventas_cliente = [venta for venta in game_venta if venta["nombre_cliente"].lower() == nombre_cliente]
            if ventas_cliente:
                for venta in ventas_cliente:
                    generar_boletas(venta)
            else:
                print("No se encontraron ventas para este cliente.")
        elif opción == 7:
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

menu()
