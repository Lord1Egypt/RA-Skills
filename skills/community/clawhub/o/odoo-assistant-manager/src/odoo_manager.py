#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xmlrpc.client
import ssl
import argparse
import os
import logging
import base64
import urllib.request
from datetime import date, timedelta

# ==========================================
# CONFIGURACIÓN DE LOGGING
# ==========================================# Configurar logging
logging.basicConfig(
    level=logging.WARNING,  # Cambiado a WARNING para evitar ruido en stdout/stderr
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==========================================
# CONFIGURACIÓN DE CONEXIÓN (solo variables de entorno; nunca credenciales en el código)
# ==========================================
def _odoo_creds():
    url = os.getenv('ODOO_URL')
    db = os.getenv('ODOO_DB')
    user = os.getenv('ODOO_USER')
    pwd = os.getenv('ODOO_PASS') or os.getenv('ODOO_PASSWORD')
    return url, db, user, pwd


# Etiqueta en informes (opcional)
STORE_LABEL = os.getenv('ODOO_STORE_LABEL', 'Store')

# Rellenados en connect() para execute_kw (XML-RPC)
DB = None
PASS = None

# ==========================================
# CONSTANTES DE NEGOCIO (IDs FIJOS)
# ==========================================
# IDs de tu base Odoo (ajusta por entorno; valores por defecto solo como ejemplo de instalación típica)
TAX_ID = int(os.getenv('ODOO_TAX_ID', '50'))
LOCATION_ID = int(os.getenv('ODOO_STOCK_LOCATION_ID', os.getenv('ODOO_LOCATION_ID', '8')))
DEFAULT_CATEGORY = int(os.getenv('ODOO_DEFAULT_CATEGORY_ID', '327'))

# IDs de Atributos de Producto
ATTR_AGE = 7          # Edad mínima
ATTR_MIN_PLAYERS = 8  # Mínimo de Jugadores  
ATTR_TIME = 9         # Tiempo de juego
ATTR_MAX_PLAYERS = 10 # Máximo de Jugadores

# Mapeo de valores de atributos (edad mínima)
AGE_VALUES = {
    '2': 178, '3': 167, '4': 147, '5': 135, '6': 134, '7': 138,
    '8': 125, '9': 172, '10': 129, '12': 114, '14': 118
}

# Mapeo de valores de atributos (mínimo jugadores)
MIN_PLAYERS_VALUES = {
    '1': 120, '2': 115, '3': 131, '4': 136, '5': 153, '6': 174, '8': 154
}

# Mapeo de valores de atributos (tiempo de juego)
TIME_VALUES = {
    '5"': 221, '10"': 140, '15"': 126, '20"': 132, '25"': 220,
    '30"': 119, '40"': 139, '45': 121, '60"': 116
}

# Mapeo de valores de atributos (máximo jugadores)
MAX_PLAYERS_VALUES = {
    '2': 128, '3': 146, '4': 117, '5': 122,
    '6': 133, '7': 158, '8': 137, '10': 149
}

# ==========================================
# MAPA DE CATEGORÍAS (TAXONOMÍA COMPLETA)
# ==========================================
# El script buscará si la "keyword" está en la categoría solicitada.
# El orden es importante: las más específicas primero.
CATEGORY_MAP = {
    # --- TCG (Cartas Coleccionables) ---
    'lorcana': 342,
    'disney': 342,
    'star wars unlimited': 343,
    'unlimited': 343,
    'mandalorian': 340,
    'one piece': 346,
    'luffy': 346,
    'pokemon': 338,
    'dragon ball': 339,
    'goku': 339,
    'magic': 337,
    'mtg': 337,
    'tcg': 337,

    # --- JUEGOS DE MESA ---
    'tablero': 329,
    'board': 329,
    'catan': 329,
    'carcassonne': 329,
    'cartas': 328,        # Juegos tipo Virus (No TCG)
    'deck': 328,
    'ingenio': 330,
    'escape': 330,
    'puzzle': 330,
    'inserto': 341,
    'organizador': 341,
    'funda': 331,
    'accesorio': 331,
    'dado': 331,

    # --- HAMA BEADS ---
    'hama midi': 334,
    'midi': 334,
    'hama mini': 335,
    'mini beads': 335,
    'placa hama': 336,
    'pinza': 336,
    'hama': 333,          # Genérico si no especifica tamaño

    # --- MERCH Y ROPA ---
    'camiseta': 349,
    't-shirt': 349,
    'ropa': 344,
    'gorra': 344,
    'sudadera': 344,
    'funko': 345,
    'merch': 345,
    'taza': 345,
    'figura': 345,
    
    # --- CULTURA POP ---
    'manga': 347,
    'anime': 347,
    'videojuego': 347,
    'cine': 348,
    'serie': 348,
    'pelicula': 348,

    # --- OTROS ---
    'evento': 332,
    'torneo': 332,
    'entrada': 332
}

# Mapa de Categorías WEB (eCommerce)
# Basado en IDs de product.public.category obtenidos
WEB_CATEGORY_MAP = {
    # TCG
    'lorcana': 50,
    'star wars unlimited': 53,
    'swu': 53,
    'unlimited': 53,
    'mandalorian': 54,
    'one piece': 51,
    'pokemon': 52,
    'dragon ball': 49,
    'tcg': 48,
    'magic': 48, # Fallback a TCG general

    # JUEGOS DE MESA
    'cartas': 42,
    'deck': 42,
    'tablero': 44,
    'board': 44,
    'catan': 44,
    'ingenio': 43,
    'escape': 43,
    'puzzle': 43,
    'accesorios': 40,
    'funda': 40,
    'dado': 40,
    'inserto': 41,

    # HAMA
    'hama': 35,
    'midi': 37,
    'mini': 38,
    
    # OTROS
    'oferta': 66,
    'evento': 34
}

# ==========================================
# LÓGICA DEL CLIENTE ODOO
# ==========================================

def connect():
    """Establece conexión SSL segura con Odoo XML-RPC"""
    global DB, PASS
    url, db, user, pwd = _odoo_creds()
    if not all([url, db, user, pwd]):
        raise ValueError(
            "Faltan credenciales Odoo. Define ODOO_URL, ODOO_DB, ODOO_USER y ODOO_PASS (o ODOO_PASSWORD)."
        )
    DB, PASS = db, pwd
    # Cloudflare DNS-Only permite el contexto por defecto sin hacks
    context = ssl.create_default_context()
    
    try:
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=context)
        uid = common.authenticate(db, user, pwd, {})
        if not uid:
            raise Exception("Autenticación fallida. Revisa Usuario/Contraseña.")
        
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=context)
        logger.info(f"✅ Conectado a {url} como {user}")
        return uid, models
    except Exception as e:
        logger.error(f"Error de Conexión: {str(e)}")
        exit(1)

def get_web_category_id(hint):
    """Devuelve listado de IDs para public_categ_ids basado en hint"""
    # Búsqueda exacta
    hint_lower = str(hint).lower().strip()
    if hint_lower in WEB_CATEGORY_MAP:
        return [WEB_CATEGORY_MAP[hint_lower]]
    
    # Búsqueda parcial
    for key, val in WEB_CATEGORY_MAP.items():
        if key in hint_lower:
            return [val]
            
    # Default: Juegos de Mesa y Cartas (39 - Padre)
    return [39]

def get_category_id(hint):
    """Devuelve el ID de categoría basado en palabras clave"""
    if not hint:
        return DEFAULT_CATEGORY
    
    hint_lower = hint.lower()
    for key, cat_id in CATEGORY_MAP.items():
        if key in hint_lower:
            return cat_id
            
    return DEFAULT_CATEGORY

def download_and_encode_image(image_url):
    """
    Descarga una imagen desde URL y la convierte a base64 para Odoo.
    
    Args:
        image_url (str): URL de la imagen a descargar
        
    Returns:
        str: Imagen codificada en base64, o None si falla
    """
    if not image_url or image_url in ["", "None"]:
        return None
        
    try:
        logger.info(f"Descargando imagen desde: {image_url[:80]}...")
        
        # Descargar imagen con timeout de 10 segundos
        req = urllib.request.Request(
            image_url,
            headers={'User-Agent': 'Mozilla/5.0 (OdooStoreManager/1.1)'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            image_data = response.read()
            
        # Validar que sea una imagen (mínimo 1KB, máximo 5MB)
        size_kb = len(image_data) / 1024
        if size_kb < 1:
            logger.warning("Imagen demasiado pequeña (< 1KB)")
            return None
        if size_kb > 5120:  # 5MB
            logger.warning(f"Imagen muy grande ({size_kb:.0f}KB), puede tardar en cargar")
        
        # Codificar a base64
        encoded = base64.b64encode(image_data).decode('utf-8')
        logger.info(f"✅ Imagen descargada y codificada ({size_kb:.0f}KB)")
        return encoded
        
    except urllib.error.HTTPError as e:
        logger.error(f"Error HTTP al descargar imagen: {e.code} {e.reason}")
        return None
    except urllib.error.URLError as e:
        logger.error(f"Error de conexión: {e.reason}")
        return None
    except Exception as e:
        logger.error(f"Error procesando imagen: {str(e)}")
        return None

def process_extra_images(product_tmpl_id, urls_str):
    """Procesa e importa imágenes secundarias (product.image)"""
    if not urls_str:
        return
        
    uid, models = connect()
    urls = [u.strip() for u in urls_str.split(',') if u.strip()]
    
    count = 0
    for idx, url in enumerate(urls):
        try:
            logger.info(f"Procesando imagen extra: {url}")
            b64_img = download_and_encode_image(url)
            if b64_img:
                models.execute_kw(DB, uid, PASS, 'product.image', 'create', [{
                    'product_tmpl_id': product_tmpl_id,
                    'name': f"Imagen Extra {idx+1}",
                    'image_1920': b64_img
                }])
                count += 1
        except Exception as e:
            logger.error(f"Error añadiendo imagen extra {url}: {e}")
            
    logger.info(f"✅ Se añadieron {count} imágenes extra al producto {product_tmpl_id}")

def build_attribute_lines(min_age, players, time):
    """
    Construye attribute_line_ids para asignar atributos al producto.
    
    Args:
        min_age (str): Edad mínima (ej: "8", "10", "14")
        players (str): Jugadores (ej: "2", "2-4", "2-6")
        time (str): Tiempo de juego (ej: "15", "30", "45")
        
    Returns:
        list: Lista de tuplas para attribute_line_ids en formato Odoo
    """
    lines = []
    
    # 1. Edad mínima
    age_value_id = AGE_VALUES.get(str(min_age))
    if age_value_id:
        lines.append((0, 0, {
            'attribute_id': ATTR_AGE,
            'value_ids': [(6, 0, [age_value_id])]
        }))
    
    # 2. Parsear jugadores (puede ser "2" o "2-4" o "2-6")
    if '-' in players:
        parts = players.split("-")
        min_p = parts[0].strip()
        max_p = parts[1].strip()
    else:
        min_p = players.strip()
        max_p = players.strip()
    
    # Mínimo de jugadores
    min_player_value_id = MIN_PLAYERS_VALUES.get(min_p)
    if min_player_value_id:
        lines.append((0, 0, {
            'attribute_id': ATTR_MIN_PLAYERS,
            'value_ids': [(6, 0, [min_player_value_id])]
        }))
    
    # Máximo de jugadores
    max_player_value_id = MAX_PLAYERS_VALUES.get(max_p)
    if max_player_value_id:
        lines.append((0, 0, {
            'attribute_id': ATTR_MAX_PLAYERS,
            'value_ids': [(6, 0, [max_player_value_id])]
        }))
    
    # 3. Tiempo de juego (añadir comillas si es necesario)
    time_str = time.strip()
    if not time_str.endswith('"'):
        time_str = time_str + '"'
    
    time_value_id = TIME_VALUES.get(time_str)
    if time_value_id:
        lines.append((0, 0, {
            'attribute_id': ATTR_TIME,
            'value_ids': [(6, 0, [time_value_id])]
        }))
    
    return lines

def check_sales():
    """Consulta ventas de TPV hoy y pedidos Web pendientes"""
    uid, models = connect()
    today = str(date.today())
    
    # 1. TPV (POS) - Ventas de hoy
    pos_domain = [
        ['date_order', '>=', today + ' 00:00:00'],
        ['date_order', '<=', today + ' 23:59:59'],
        ['state', 'in', ['paid', 'done', 'invoiced']]
    ]
    # Suma rápida usando read_group
    pos_data = models.execute_kw(DB, uid, PASS, 'pos.order', 'read_group', 
        [pos_domain, ['amount_total'], []])
    
    pos_total = pos_data[0]['amount_total'] if pos_data else 0.0
    pos_count = models.execute_kw(DB, uid, PASS, 'pos.order', 'search_count', [pos_domain])

    # 2. WEB - Pedidos pendientes (Compatible Odoo 14-18)
    web_domain = [
        ['state', '=', 'sale'],              # Confirmado
        ['website_id', '!=', False],         # Origen Web
        ['picking_ids.state', 'not in', ['done', 'cancel']]  # No entregado/cancelado
    ]
    
    web_ids = models.execute_kw(DB, uid, PASS, 'sale.order', 'search', [web_domain])
    
    # GENERAR REPORTE
    report = f"📊 **REPORTE {STORE_LABEL.upper()} ({today})**\n"
    report += f"💰 **Caja TPV:** {pos_total:.2f}€ ({pos_count} tickets)\n"
    
    if not web_ids:
        report += "✅ Todo tranquilo. No hay pedidos web pendientes de envío."
    else:
        report += f"📦 **{len(web_ids)} PEDIDOS WEB PENDIENTES:**\n"
        orders = models.execute_kw(DB, uid, PASS, 'sale.order', 'read', [web_ids], 
            {'fields': ['name', 'partner_id', 'amount_total', 'partner_shipping_id', 'order_line']})
        
        for o in orders:
            # Obtener dirección simplificada (con validación)
            shipping_data = models.execute_kw(DB, uid, PASS, 'res.partner', 'read', 
                [o['partner_shipping_id'][0]], {'fields': ['city', 'zip']})
            shipping = shipping_data[0] if shipping_data else {}
            city = shipping.get('city', 'Sin ciudad')
            
            report += f"\n🔸 **{o['name']}** | {o['partner_id'][1]} ({city})\n"
            
            # Líneas del pedido
            lines = models.execute_kw(DB, uid, PASS, 'sale.order.line', 'read', [o['order_line']], {'fields': ['name', 'product_uom_qty']})
            for l in lines:
                # Limpiamos el nombre del producto (quita corchetes [REF])
                prod_name = l['name'].split(']')[1].strip() if ']' in l['name'] else l['name']
                report += f"   - {int(l['product_uom_qty'])}x {prod_name[:40]}...\n"

    return report

def get_web_orders():
    """Consulta pedidos web pendientes de envío"""
    uid, models = connect()
    
    # Buscar pedidos de venta (sale.order) confirmados con entregas pendientes
    # state='sale' = Confirmado, state='done' = Bloqueado (completado pero puede tener envíos pendientes)
    try:
        orders = models.execute_kw(DB, uid, PASS, 'sale.order', 'search_read',
            [[
                ('state', 'in', ['sale', 'done']),  # Pedidos confirmados/completados
                ('picking_ids.state', 'not in', ['done', 'cancel'])  # Con entregas NO completadas
            ]],
            {'fields': ['name', 'partner_id', 'amount_total', 'date_order', 'state'],
             'order': 'date_order desc',
             'limit': 50})
    except Exception as e:
        logger.error(f"Error consultando pedidos web: {e}")
        return "❌ Error al consultar pedidos web"
    
    if not orders:
        return "✅ No hay pedidos web pendientes de envío"
    
    # Formatear salida conversacional
    total_amount = sum(o['amount_total'] for o in orders)
    result = f"📦 **{len(orders)} pedido(s) web pendiente(s)** (Total: {total_amount:.2f}€)\n\n"
    
    for order in orders:
        customer = order['partner_id'][1] if order['partner_id'] else 'Cliente desconocido'
        result += f"- **{order['name']}**: {customer} - {order['amount_total']:.2f}€\n"
    
    return result

def parse_price(price_input):
    """Convierte input de precio (str o float) a float seguro"""
    if isinstance(price_input, (float, int)):
        return float(price_input)
    
    if isinstance(price_input, str):
        # Reemplazar coma por punto
        clean_price = price_input.replace(',', '.')
        # Si hay múltiples puntos, dejar solo el último (ej: 1.000.50 -> 1000.50)
        if clean_price.count('.') > 1:
            clean_price = clean_price.replace('.', '', clean_price.count('.') - 1)
        return float(clean_price)
    
    return 0.0

def add_product(name, price, qty, barcode, category_hint, min_age, players, time, description, image_url="", extra_images=""):
    """Crea o actualiza productos con lógica de negocio"""
    uid, models = connect()
    
    # Normalizar precio
    try:
        final_price = parse_price(price)
    except ValueError:
        return f"❌ Error: El precio '{price}' no es válido."
    
    # 1. Determinar Categoría ID
    categ_id = get_category_id(category_hint)
    
    # 2. Buscar Producto Existente (Upsert)
    product_id = False
    
    # A) Por Código de Barras (Prioridad)
    if barcode and barcode not in ["None", "Unknown", ""]:
        ids = models.execute_kw(DB, uid, PASS, 'product.template', 'search', [[['barcode', '=', barcode]]])
        if ids: product_id = ids[0]
    
    # B) Por Nombre Exacto
    if not product_id:
        ids = models.execute_kw(DB, uid, PASS, 'product.template', 'search', [[['name', '=', name]]])
        if ids: product_id = ids[0]

    # --- LÓGICA DE STOCK (No aplicable para type='consu') ---
    def update_stock_quant(tmpl_id, quantity):
        """
        NOTA: Freakmondo usa productos tipo 'consu' (consumibles) que no requieren
        gestión de stock.quant. La cantidad se gestiona directamente en el producto.
        """
        try:
            # Para consumibles, actualizamos qty_available en product.product
            p_ids = models.execute_kw(DB, uid, PASS, 'product.product', 'search', 
                [[['product_tmpl_id', '=', tmpl_id]]])
            if not p_ids: 
                logger.warning("No se encontró variante del producto")
                return "⚠️ Error: No encuentro variante."
            variant_id = p_ids[0]
            
            # Nota: qty_available es computed, no se puede setear directamente
            # Para consumibles, el stock no se rastrea en Odoo
            logger.info(f"Producto consumible creado (stock manual en TPV)")
            return f"Stock configurado: {quantity} u. (gestión manual en TPV)"
        except Exception as e:
            logger.error(f"Info de stock: {e}")
            return f"Stock: {quantity} u. (gestión manual)"

    # --- HTML DESCRIPCIÓN ---
    # 1. Determinar Categoría ID (Interna)
    categ_id = get_category_id(category_hint)
    
    # 2. Determinar Categoría WEB
    web_categ_ids = get_web_category_id(category_hint)

    web_html = f"""
    <div class="product-description-wrapper">
        <div class="product-intro">
            {description}
        </div>
        <hr/>
        <div class="product-specs">
            <h3>📋 Ficha Técnica</h3>
            <ul>
                <li><strong>👥 Jugadores:</strong> {players}</li>
                <li><strong>⏳ Duración:</strong> {time} min</li>
                <li><strong>👶 Edad mínima:</strong> {min_age}+</li>
            </ul>
        </div>
    </div>
    """

    # --- EJECUCIÓN ---
    if product_id:
        # ACTUALIZAR
        vals = {
            'list_price': final_price,
            'taxes_id': [(6, 0, [TAX_ID])], # Aseguramos que tenga IVA bien puesto
            'public_categ_ids': [(6, 0, web_categ_ids)] # Actualizar categoría web
        }
        
        # Actualizar Imagen Principal si se provee
        if image_url:
            b64 = download_and_encode_image(image_url)
            if b64:
                vals['image_1920'] = b64
        
        models.execute_kw(DB, uid, PASS, 'product.template', 'write', [[product_id], vals])
        stock_msg = update_stock_quant(product_id, qty)
        
        # Procesar Imágenes Extra
        if extra_images:
            process_extra_images(product_id, extra_images)
        
        # Obtenemos nombre de categoría para informar (con validación)
        cat_data = models.execute_kw(DB, uid, PASS, 'product.public.category', 'read', 
            [web_categ_ids[0]], {'fields': ['name']})
        cat_name = cat_data[0]['name'] if cat_data else 'Desconocida'
        
        logger.info(f"Producto actualizado: {name}")
        return f"🔄 **ACTUALIZADO:** {name}\n- Precio: {final_price}€\n- Categoría Web: {cat_name}\n- {stock_msg}"
        
    else:
        # CREAR
        vals = {
            'name': name,
            'list_price': final_price,
            'type': 'consu',    # En Odoo 18+, 'consu' = Goods.
            'is_storable': True, # Esto define si es Almacenable
            'tracking': 'none', 
            'barcode': barcode if barcode not in ["None", ""] else False,
            'default_code': barcode if barcode not in ["None", ""] else False,
            'categ_id': categ_id,
            'public_categ_ids': [(6, 0, web_categ_ids)],
            'taxes_id': [(6, 0, [TAX_ID])],
            'description_ecommerce': web_html,
            'website_published': True,
            'available_in_pos': True,
            'attribute_line_ids': build_attribute_lines(min_age, players, time),
        }
        
        # Procesar y añadir imagen si se proporcionó URL
        if image_url:
            image_b64 = download_and_encode_image(image_url)
            if image_b64:
                vals['image_1920'] = image_b64

        try:
            new_id = models.execute_kw(DB, uid, PASS, 'product.template', 'create', [vals])
            
            # Usar la función global update_stock (ya que ahora sí es product)
            # Pasamos name porque update_stock busca por name/ref
            stock_msg = update_stock(name, qty)
            
            # --- IMÁGENES SECUNDARIAS ---
            if extra_images:
                process_extra_images(new_id, extra_images)
            
            logger.info(f"Producto creado: {name} (ID: {new_id})")
            return f"✅ **CREADO:** {name} (ID: {new_id})\n- Precio: {price}€\n- {stock_msg}\n- Categoría ID: {categ_id}"
        except Exception as e:
            logger.error(f"Error creando producto: {str(e)}")
            return f"❌ Error Crítico Odoo: {str(e)}"

def check_stock(query):
    """Busca productos por nombre o código y devuelve info rápida"""
    uid, models = connect()
    
    # Buscar (limit 20)
    domain = ['|', ['barcode', '=', query], ['name', 'ilike', query]]
    p_ids = models.execute_kw(DB, uid, PASS, 'product.product', 'search', [domain], {'limit': 20})
    
    if not p_ids:
        return f"❌ No encuentro nada que coincida con '{query}'."
    
    # Leer datos
    products = models.execute_kw(DB, uid, PASS, 'product.product', 'read', [p_ids], 
        {'fields': ['name', 'list_price', 'qty_available', 'virtual_available']})
        
    msg = ""
    if len(products) == 1:
        p = products[0]
        msg = (
            f"✅ **{p['name']}**\n"
            f"💰 PVP: {p['list_price']}€\n"
            f"📦 Stock Físico: {int(p['qty_available'])}\n"
            f"📅 Previsto: {int(p['virtual_available'])}"
        )
    else:
        msg = f"🔎 **Encontré {len(products)} coincidencias:**\n"
        for p in products:
            msg += f"- **{p['name']}**: {int(p['qty_available'])} uds. ({p['list_price']}€)\n"
            
    return msg

def update_stock(ref, quantity):
    """Actualiza stock usando is_storable (Odoo 18)"""
    uid, models = connect()
    quantity = float(quantity)

    # 1. Buscar producto (Product Product, no Template)
    domain = ['|', ['barcode', '=', ref], ['name', 'ilike', ref]]
    p_ids = models.execute_kw(DB, uid, PASS, 'product.product', 'search', [domain])
    
    if not p_ids:
        return f"❌ No encuentro el producto '{ref}'."
    
    product_id = p_ids[0]
    # Check is_storable AND type
    product = models.execute_kw(DB, uid, PASS, 'product.product', 'read', [product_id], {'fields': ['name', 'type', 'is_storable']})[0]
    
    p_type = product.get('type')
    is_storable = product.get('is_storable') # Booleano o None
    name = product['name']

    # Lógica Odoo 18:
    if is_storable is not None:
        if not is_storable:
             # Auto-Fix Odoo 18
             try:
                models.execute_kw(DB, uid, PASS, 'product.product', 'write', [[product_id], {'is_storable': True}])
                logger.info(f"🔧 [Odoo 18] Activado is_storable para '{name}'")
             except Exception as e:
                return f"⚠️ Falló conversión is_storable: {e}"
    
    # Lógica Legacy (si is_storable no existe):
    elif p_type == 'consu':
         return f"⚠️ '{name}' es un CONSUMIBLE (Legacy). No gestiona stock."
    
    if p_type == 'service':
         return f"⚠️ '{name}' es un SERVICIO."

    # 2. Actualizar Stock.Quant (Ubicación 8 = Stock)
    quant_domain = [['product_id', '=', product_id], ['location_id', '=', LOCATION_ID]]
    quant_ids = models.execute_kw(DB, uid, PASS, 'stock.quant', 'search', [quant_domain])
    
    try:
        if quant_ids:
            # Odoo 16+: inventory_quantity + action_apply_inventory
            models.execute_kw(DB, uid, PASS, 'stock.quant', 'write', [quant_ids, {'inventory_quantity': quantity}])
            
            # Odoo 18 bug workaround: action_apply_inventory returns None triggering XMLRPC error
            try:
                models.execute_kw(DB, uid, PASS, 'stock.quant', 'action_apply_inventory', [quant_ids])
            except Exception as e:
                if "cannot marshal None" not in str(e): raise e

        else:
            # Crear nuevo quant
            models.execute_kw(DB, uid, PASS, 'stock.quant', 'create', [{
                'product_id': product_id,
                'location_id': LOCATION_ID,
                'inventory_quantity': quantity
            }])
            # Aplicar
            quant_ids = models.execute_kw(DB, uid, PASS, 'stock.quant', 'search', [quant_domain])
            if quant_ids:
                try:
                    models.execute_kw(DB, uid, PASS, 'stock.quant', 'action_apply_inventory', [quant_ids])
                except Exception as e:
                    if "cannot marshal None" not in str(e): raise e
                
        return f"✅ Stock de **{name}** actualizado a **{int(quantity)}** unidades."
        
    except Exception as e:
        logger.error(f"Error actualizando stock: {e}")
        return f"❌ Error Odoo intentando actualizar stock: {e}"

def get_top_sales(period):
    """Obtiene top ventas del periodo indicado"""
    uid, models = connect()
    today = date.today()
    
    if 'año' in period or 'year' in period:
        days = 365
        label = "Último Año"
    elif '2' in period:
        days = 60
        label = "Últimos 2 Meses"
    elif 'semana' in period:
        days = 7
        label = "Última Semana"
    else:
        days = 30
        label = "Último Mes"
        
    start_date = str(today - timedelta(days=days))
    
    # 1. Consultar VENTAS WEB / BACKEND (sale.order.line)
    sale_domain = [
        ['state', 'in', ['sale', 'done']],
        ['order_id.date_order', '>=', start_date]
    ]
    
    product_sales = {} # {product_id: {'name': name, 'qty': qty}}

    try:
        # Ventas Normales
        sale_groups = models.execute_kw(DB, uid, PASS, 'sale.order.line', 'read_group', 
            [sale_domain, ['product_uom_qty'], ['product_id']], {'lazy': False})
            
        for g in sale_groups:
            if not g['product_id']: continue
            pid = g['product_id'][0]
            name = g['product_id'][1]
            qty = g['product_uom_qty']
            
            if pid not in product_sales:
                product_sales[pid] = {'name': name, 'qty': 0}
            product_sales[pid]['qty'] += qty

        # 2. Consultar PUNTO DE VENTA (pos.order.line)
        # Nota: POS usa 'qty' en lugar de 'product_uom_qty' y 'order_id.date_order'
        pos_domain = [
            ['state', 'in', ['paid', 'done', 'invoiced']], # POS states
            ['order_id.date_order', '>=', start_date]
        ]
        
        # En POS a veces state está en order_id, no en line. Check pos.order state.
        # Domain filtering on relation order_id.state works.
        # pos.order.line doesn't have state? pos.order does.
        # Let's filter by order_id.date_order.
        pos_line_domain = [['order_id.date_order', '>=', start_date], ['order_id.state', 'in', ['paid', 'done', 'invoiced']]]
        
        pos_groups = models.execute_kw(DB, uid, PASS, 'pos.order.line', 'read_group', 
             [pos_line_domain, ['qty'], ['product_id']], {'lazy': False})
             
        for g in pos_groups:
            if not g['product_id']: continue
            pid = g['product_id'][0]
            name = g['product_id'][1]
            qty = g['qty']
            
            if pid not in product_sales:
                product_sales[pid] = {'name': name, 'qty': 0}
            product_sales[pid]['qty'] += qty

        # Ordenar Top 50
        sorted_products = sorted(product_sales.values(), key=lambda x: x['qty'], reverse=True)[:50]

        if not sorted_products:
            return f"📉 No hay ventas (Web ni TPV) registradas en: {label}"
            
        report = f"📊 **TOP VENTAS GLOBAL ({label})**\n\n"
        for idx, p in enumerate(sorted_products):
            report += f"{idx+1}. **{int(p['qty'])}**x {p['name']}\n"
            
        return report

    except Exception as e:
        logger.error(f"Error top ventas: {e}")
        return f"❌ Error consultando ventas: {e}"

def get_order_details(order_name):
    uid, models = connect()

    # 1. Buscar el ID del pedido por su nombre
    order_ids = models.execute_kw(DB, uid, PASS, 'sale.order', 'search', [[('name', '=', order_name)]])

    if not order_ids:
        return f"❌ No se encontró el pedido '{order_name}'."
    else:
        order_id = order_ids[0]

        # 2. Leer los detalles del pedido, incluyendo las líneas del pedido
        order = models.execute_kw(DB, uid, PASS, 'sale.order', 'read', [order_id],
            {'fields': ['name', 'partner_id', 'amount_total', 'order_line', 'partner_shipping_id']})[0]

        # 2.5. Leer los detalles de la dirección de envío si existe
        shipping_address = {}
        if order['partner_shipping_id']:
            shipping_partner_id = order['partner_shipping_id'][0]
            shipping_data = models.execute_kw(DB, uid, PASS, 'res.partner', 'read', [shipping_partner_id],
                {'fields': ['street', 'street2', 'zip', 'city', 'state_id', 'country_id', 'phone', 'mobile']})
            if shipping_data: shipping_address = shipping_data[0]

        # 3. Leer los detalles de cada línea del pedido
        lines = models.execute_kw(DB, uid, PASS, 'sale.order.line', 'search_read', [[('id', 'in', order['order_line'])]],
            {'fields': ['name', 'product_uom_qty', 'price_unit']})

        result = f"📋 **Detalle del Pedido '{order_name}' de {order['partner_id'][1]}**\n"
        result += f"💰 Total: {order['amount_total']:.2f}€\n"

        if shipping_address:
            street = shipping_address.get('street', '')
            street2 = shipping_address.get('street2', '')
            zip_code = shipping_address.get('zip', '')
            city = shipping_address.get('city', '')
            state = shipping_address['state_id'][1] if shipping_address.get('state_id') else ''
            country = shipping_address['country_id'][1] if shipping_address.get('country_id') else ''
            
            result += "\n🚚 **Dirección de Envío:**\n"
            result += f"   - {street} {street2}\n" if street2 else f"   - {street}\n"
            result += f"   - {zip_code} {city}\n"
            result += f"   - {state}, {country}\n"
            
            phone = shipping_address.get('phone')
            mobile = shipping_address.get('mobile')
            
            if phone: result += f"   - Teléfono: {phone}\n"
            if mobile and mobile != phone: result += f"   - Móvil: {mobile}\n"
        
        result += "\n📦 **Productos:**\n"

        for l in lines:
            prod_name = l['name'].split(']')[1].strip() if ']' in l['name'] else l['name']
            result += f"- {int(l['product_uom_qty'])}x {prod_name} ({l['price_unit']:.2f}€/u)\n"

        return result

def get_event_registrations(event_name):
    uid, models = connect()

    # 1. Buscar el evento por su nombre
    event_ids = models.execute_kw(DB, uid, PASS, 'event.event', 'search', [[('name', 'ilike', event_name)]])

    if not event_ids:
        return f"❌ No se encontró ningún evento con el nombre '{event_name}'."
    else:
        event_id = event_ids[0]
        event_data = models.execute_kw(DB, uid, PASS, 'event.event', 'read', [event_id], {'fields': ['name']})[0]
        
        # 2. Contar las inscripciones para ese evento
        registration_count = models.execute_kw(DB, uid, PASS, 'event.registration', 'search_count', [[('event_id', '=', event_id)]])
        
        return f"🎉 Para el evento **'{event_data['name']}'** hay **{registration_count}** personas apuntadas."

# ==========================================
# GESTIÓN DE ARGUMENTOS (CLI)
# ==========================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Odoo Store Manager (XML-RPC CLI)")
    subparsers = parser.add_subparsers(dest="command")

    # 1. CHECK SALES
    subparsers.add_parser("check_sales")

    # 2. WEB ORDERS
    subparsers.add_parser("web_orders", help="Consultar pedidos web pendientes de envío")

    # 3. ADD PRODUCT
    add = subparsers.add_parser("add_product")
    add.add_argument("--name", required=True, help="Nombre del producto")
    add.add_argument("--price", required=True, help="Precio PVP (acepta coma o punto)")
    add.add_argument("--qty", required=True, type=float, help="Cantidad de stock")
    add.add_argument("--barcode", default="", help="Código de barras EAN")
    add.add_argument("--category", default="generic", help="Palabra clave para categorizar (ej: lorcana, tablero)")
    add.add_argument("--min_age", default="8", help="Edad mínima")
    add.add_argument("--players", default="2-4", help="Número de jugadores")
    add.add_argument("--time", default="30", help="Tiempo de juego")
    add.add_argument("--description", default="Juego de mesa", help="Descripción comercial para la web")
    add.add_argument("--image-url", default="", help="URL de la imagen del producto")
    add.add_argument("--extra-images", default="", help="URLs de imágenes extra separadas por coma")

    # 4. UPDATE STOCK
    stock = subparsers.add_parser("update_stock")
    stock.add_argument("--ref", help="Referencia, Código o Nombre")
    stock.add_argument("--barcode", dest="ref_alias_1", help="Alias de ref")
    stock.add_argument("--name", dest="ref_alias_2", help="Alias de ref")
    stock.add_argument("--qty", required=True, help="Nueva cantidad de stock")

    # 5. TOP SALES
    sales = subparsers.add_parser("top_sales")
    sales.add_argument("--period", default="mes", help="Periodo (mes, 2, año)")

    # 6. CHECK STOCK
    check = subparsers.add_parser("check_stock")
    check.add_argument("--query", help="Nombre o código a buscar")
    check.add_argument("--name", dest="query_alias", help="Alias de query")
    
    # 7. GET ORDER DETAILS
    details = subparsers.add_parser("get_order_details", help="Obtener detalles de un pedido por su nombre")
    details.add_argument("--name", required=True, help="Nombre del pedido (ej: S00352)")

    # 8. GET EVENT REGISTRATIONS
    event_reg = subparsers.add_parser("get_event_registrations", help="Obtener el número de inscripciones para un evento")
    event_reg.add_argument("--name", required=True, help="Nombre del evento (ej: Lorcana Whisperbell)")

    args = parser.parse_args()
    
    # Normalizar args de check_stock
    if args.command == "check_stock":
        final_query = args.query or args.query_alias
        if not final_query:
            parser.error("check_stock requiere --query o --name")
        args.query = final_query

    if args.command == "check_sales":
        print(check_sales())
    elif args.command == "web_orders":
        print(get_web_orders())
    elif args.command == "add_product":
        print(add_product(
            args.name, args.price, args.qty, args.barcode, args.category,
            args.min_age, args.players, args.time,
            args.description, args.image_url, args.extra_images
        ))
    elif args.command == "update_stock":
        final_ref = args.ref or args.ref_alias_1 or args.ref_alias_2
        if not final_ref:
             parser.error("update_stock requiere --ref, --barcode o --name")
        print(update_stock(final_ref, args.qty))
        
    elif args.command == "top_sales":
        print(get_top_sales(args.period))
        
    elif args.command == "check_stock":
        print(check_stock(args.query))
    elif args.command == "get_order_details":
        print(get_order_details(args.name))
    elif args.command == "get_event_registrations":
        print(get_event_registrations(args.name))
    else:
        parser.print_help()