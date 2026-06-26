#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xmlrpc.client
import ssl
import time
import os
import subprocess
import shlex
import logging
import requests
import re
# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==========================================
# CONFIGURACIÓN (solo entorno; nunca credenciales en el código)
# ==========================================
URL = os.getenv('ODOO_URL')
DB = os.getenv('ODOO_DB')
USER = os.getenv('ODOO_USER')
PASS = os.getenv('ODOO_PASS') or os.getenv('ODOO_PASSWORD')
BOT_PARTNER_ID_RAW = os.getenv('ODOO_BOT_PARTNER_ID')

def connect():
    """Conexión segura SSL con Odoo"""
    context = ssl.create_default_context()
    try:
        common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common', context=context)
        uid = common.authenticate(DB, USER, PASS, {})
        models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object', context=context)
        return uid, models
    except Exception as e:
        logger.error(f"❌ Error conectando a Odoo: {e}")
        return None, None

def run_manager_tool(command_args):
    """
    Ejecuta el script `odoo_manager.py` que está en la misma carpeta
    y devuelve la salida de texto.
    
    Args:
        command_args (str): Argumentos para el script (ej: "check_sales", "web_orders")
    """
    start_time = time.time()
    try:
        # Ruta absoluta al script manager
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, 'odoo_manager.py')
        
        # Construimos el comando: python3 script.py argumento
        # Usamos shlex.split para seguridad, pero command_args son controlados por nosotros
        cmd = ["python3", script_path] + shlex.split(command_args)
        
        logger.debug(f"⚙️ Ejecutando: {' '.join(cmd)}")
        
        # Ejecutamos y capturamos el output con timeout de 30s
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=30)
        output = result.decode('utf-8')
        
        elapsed = time.time() - start_time
        logger.debug(f"✅ Ejecución completada en {elapsed:.2f}s. Salida: {len(output)} chars")
        
        return output
        
    except subprocess.TimeoutExpired:
        logger.error("⚠️ Timeout ejecutando script (30s)")
        return "⚠️ Error: El comando tardó demasiado tiempo."
    except subprocess.CalledProcessError as e:
        error_msg = f"⚠️ Error ejecutando script:\n{e.output.decode('utf-8')}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"⚠️ Error inesperado: {str(e)}"
        logger.error(error_msg)
        return error_msg

def extract_metadata(url):
    """Extrae título y descripción de una URL usando requests y regex"""
    title = "Producto Importado Web"
    description = ""
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=10)
        r.encoding = r.apparent_encoding
        
        if r.status_code == 200:
            html = r.text
            
            # 1. TÍTULO (H1 o Title)
            h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
            if h1_match:
                raw_title = h1_match.group(1).strip()
                title = re.sub(r'<[^>]+>', '', raw_title)
            else:
                title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
                if title_match:
                    title = title_match.group(1).strip().split('-')[0].strip()

            # 2. DESCRIPCIÓN HTML — Intentar múltiples selectores (orden de prioridad)
            desc_selectors = [
                r'<div[^>]*class=["\'][^"\']*\bproduct-description\b[^"\']*["\'][^>]*>(.*?)</div>',
                r'<div[^>]*class=["\'][^"\']*\bdescripcion\b[^"\']*["\'][^>]*>(.*?)</div>',
                r'<div[^>]*itemprop=["\']description["\'][^>]*>(.*?)</div>',
                r'<div[^>]*id=["\']description["\'][^>]*>(.*?)</div>',
                r'<div[^>]*class=["\'][^"\']*\btab-pane\b[^"\']*["\'][^>]*id=["\'][^"\']*desc[^"\']*["\'][^>]*>(.*?)</div>',
                r'<div[^>]*class=["\'][^"\']*\bproduct_description\b[^"\']*["\'][^>]*>(.*?)</div>',
            ]
            
            for selector in desc_selectors:
                desc_match = re.search(selector, html, re.IGNORECASE | re.DOTALL)
                if desc_match:
                    raw_desc = desc_match.group(1).strip()
                    
                    # Limpiar estilos inline y clases (pero PRESERVAR estructura HTML)
                    clean_desc = re.sub(r'\s+style=["\'][^"\']*["\']', '', raw_desc, flags=re.IGNORECASE)
                    clean_desc = re.sub(r'\s+class=["\'][^"\']*["\']', '', clean_desc, flags=re.IGNORECASE)
                    # Limpiar spans vacíos
                    clean_desc = re.sub(r'<span>(.*?)</span>', r'\1', clean_desc, flags=re.IGNORECASE | re.DOTALL)
                    # Limpiar divs internos vacíos (dejar contenido)
                    clean_desc = re.sub(r'<div>(.*?)</div>', r'\1', clean_desc, flags=re.IGNORECASE | re.DOTALL)
                    
                    if len(clean_desc) > 50:
                        description = clean_desc
                        logger.info(f"📝 Descripción HTML capturada ({len(clean_desc)} chars)")
                        break

            # 3. FALLBACK: META DESCRIPCIÓN 
            if not description:
                desc_match = re.search(r'<meta\s+(?:name|property)=["\'](?:description|og:description)["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
                if desc_match:
                    raw_meta = desc_match.group(1).strip()
                    raw_meta = raw_meta.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                    # Convertir texto plano a párrafos HTML para consistencia
                    description = f"<p>{raw_meta}</p>"
                    logger.info(f"📝 Descripción meta fallback ({len(raw_meta)} chars)")
            
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
    
    return title, description

def format_response_html(text):
    """Adapta la respuesta para Odoo Discuss (Markdown con saltos dobles)."""
    return text.replace('\n', '\n\n')

def listen_loop():
    if not all([URL, DB, USER, PASS, BOT_PARTNER_ID_RAW]):
        logger.error(
            "Faltan variables: ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASS o ODOO_PASSWORD, ODOO_BOT_PARTNER_ID"
        )
        return
    bot_partner_id = int(BOT_PARTNER_ID_RAW)
    logger.info(f"🎧 Listener Odoo en {URL} (Partner ID: {bot_partner_id})...")
    uid, models = connect()
    
    if not uid:
        logger.error("❌ No se pudo conectar. Revisa usuario/contraseña.")
        return

    # Marcamos el tiempo de inicio para no responder mensajes antiguos
    # Odoo usa UTC en base de datos, pero la API suele manejar fechas string
    # Usaremos el último ID procesado para ser más seguros que la fecha
    last_processed_id = 0
    
    # Primero buscamos el último mensaje existente para empezar desde ahí
    try:
        # Búsqueda global (sin filtro de modelo) para obtener el VERDADERO último ID
        initial_search = models.execute_kw(DB, uid, PASS, 'mail.message', 'search', 
            [[]], {'limit': 1, 'order': 'id desc'})
        if initial_search:
            last_processed_id = initial_search[0]
            logger.info(f"🔄 Iniciando desde mensaje ID: {last_processed_id}")
    except Exception as e:
        logger.warning(f"No se pudo obtener último mensaje: {e}")

    while True:
        try:
            # 1. BUSCAR MENSAJES NUEVOS
            # Modificado: Buscamos TODO mensaje nuevo de tipo comentario
            # Luego filtramos en Python si es relevante
            domain = [
                ['id', '>', last_processed_id],         # Solo mensajes nuevos
                ['message_type', '=', 'comment'],       # Solo comentarios
                ['author_id', '!=', bot_partner_id]     # No auto-respuesta
            ]
            
            # Buscamos IDs de mensajes
            msg_ids = models.execute_kw(DB, uid, PASS, 'mail.message', 'search', 
                [domain], {'order': 'id asc', 'limit': 10})
            
            if msg_ids:
                logger.debug(f"🔍 Encontrados {len(msg_ids)} mensajes nuevos (IDs: {msg_ids})")
                
                # Leemos datos
                messages = models.execute_kw(DB, uid, PASS, 'mail.message', 'read', [msg_ids], 
                    {'fields': ['body', 'author_id', 'res_id', 'model', 'date', 'partner_ids', 'message_type']})
                
                for msg in messages:
                    current_id = msg['id']
                    last_processed_id = max(last_processed_id, current_id)
                    
                    author_name = msg['author_id'][1] if msg['author_id'] else "Sistema"
                    msg_type = msg.get('message_type', 'unknown')
                    model = msg.get('model', '')
                    
                    logger.debug(f"--> Procesando Msg {current_id} de {author_name} (Modelo: {model})")
                    
                    # FILTRADO DE RELEVANCIA
                    # 1. Si es DM al bot (partner_ids lo incluye) -> RELEVANTE
                    # 2. Si es en un Canal (discuss.channel) -> RELEVANTE (Analizaremos texto)
                    # 3. Otros modelos (facturas, ventas) -> IGNORAR por defecto para no spamear notas
                    
                    is_direct_mention = bot_partner_id in msg.get('partner_ids', [])
                    is_channel_chat = model == 'discuss.channel'
                    
                    if not (is_direct_mention or is_channel_chat):
                        logger.debug(f"    Ignorado: No es DM ni Chat de Canal (Modelo: {model})")
                        continue
                    
                    if msg['author_id'] and msg['author_id'][0] == bot_partner_id:
                        continue
                    
                    if author_name == "OdooBot":
                         continue

                    raw_text = msg['body'] or ""
                    # Limpieza robusta de HTML: Reemplazar <br> por espacio, y eliminar resto de tags
                    text_no_br = raw_text.replace('<br>', ' ').replace('<br/>', ' ').replace('</p>', ' ').replace('</div>', ' ')
                    clean_text = re.sub(r'<[^>]+>', '', text_no_br).strip()
                    # Reducir múltiples espacios a uno
                    clean_text = re.sub(r'\s+', ' ', clean_text)
                    clean_text_lower = clean_text.lower()
                    
                    logger.info(f"📩 Mensaje Potencial de {author_name}: {clean_text}")
                    
                    response_text = ""
                    
                    # --- CEREBRO ---
                    # Para canales públicos, SOLO respondemos si hay keyword clara
                    # Para DM, respondemos a todo (o default)
                    
                    keywords_found = False
                    
                    # COMANDO 1: CAJA / VENTAS
                    if any(x in clean_text_lower for x in ['caja', 'ventas', 'dinero']):
                        response_text = run_manager_tool("check_sales")
                        keywords_found = True
                        
                    # COMANDO 2: PEDIDOS WEB
                    elif any(x in clean_text_lower for x in ['pedidos', 'web', 'envios']):
                        response_text = run_manager_tool("web_orders")
                        keywords_found = True
                    
                    # COMANDO 3: AYUDA
                    elif "ayuda" in clean_text_lower or "help" in clean_text_lower:
                        response_text = (
                            "🤖 **Comandos disponibles:**\n"
                            "- **Caja / Ventas**\n"
                            "- **Pedidos / Web**\n"
                            "- **Ayuda**"
                        )
                        keywords_found = True
                    
                    # COMANDO 4: SALUDO
                    elif any(x in clean_text_lower for x in ['hola', 'hello', 'buenas', 'hi']):
                        response_text = f"👋 Hola, {author_name}. Escribe **ayuda** para ver comandos."
                        keywords_found = True

                    # COMANDO 5: SMART ADD (Regex)
                    # "añade [URL] ... a [PRECIO] ... en [CATEGORIA]"
                    # Regex más flexible:
                    smart_match = re.search(
                        r"añade\s+(?P<url>https?://\S+).*?a\s+(?P<price>[\d.,]+).*?en\s+(?P<category>.+)", 
                        clean_text, re.IGNORECASE | re.DOTALL
                    )
                    
                    # EXTRACTOR DE IMÁGENES (Soporte Múltiple)
                    # "con [URL1] [URL2] [URL3] a ..."
                    img_section_match = re.search(r"con\s+(?P<content>.*?)(?=\s+a\s+[\d.,]+)", clean_text, re.IGNORECASE | re.DOTALL)
                    
                    img_url = ""
                    extra_images_str = ""
                    
                    if img_section_match:
                        content = img_section_match.group('content')
                        found_urls = re.findall(r"https?://[^\s\"']+", content)
                        if found_urls:
                            img_url = found_urls[0]  # Principal
                            if len(found_urls) > 1:
                                extra_images_str = ",".join(found_urls[1:])
                                logger.info(f"📸 Imágenes extra detectadas: {len(found_urls)-1}")

                    if smart_match:
                        logger.info("🧠 Comando SMART detectado")
                        url = smart_match.group('url')
                        url = url.split('"')[0].split('<')[0]
                        
                        price = smart_match.group('price').replace(',', '.')
                        category = smart_match.group('category').strip()
                        
                        name, description = extract_metadata(url)
                        # No eliminar comillas — pueden ser parte del HTML
                        # shlex.quote se encargará de proteger el argumento
                        
                        logger.info(f"   Nombre detectado: {name}")
                        
                        # Default Qty = 0
                        qty = 0
                        
                        # EXTRACTOR DE CANTIDAD (Opcional)
                        # "con 5 unidades", "x5", "5 stock"
                        qty_match = re.search(r"(?:con|x)\s*(?P<qty>\d+)\s*(?:u\.|unidades|stock|uds)?", clean_text, re.IGNORECASE)
                        if qty_match:
                            qty = int(qty_match.group('qty'))
                            logger.info(f"📦 Cantidad inicial detectada: {qty}")

                        # Construir Comando Manager (con extra images y qty)
                        manager_cmd = (
                            f"add_product --name {shlex.quote(name)} --price {price} --qty {qty} "
                            f"--category {shlex.quote(category)} --image-url {shlex.quote(img_url)} "
                            f"--extra-images {shlex.quote(extra_images_str)} "
                            f"--description {shlex.quote(description)}"
                        )
                        
                        response_text = run_manager_tool(manager_cmd)
                        keywords_found = True

                    # COMANDO 6: UPDATE STOCK
                    # "ajusta stock [REF] a [CANTIDAD]"
                    stock_match = re.search(r"(?:ajusta|pon|cambia|actualiza)\s+stock\s+(?:de\s+)?(?P<ref>.+?)\s+a\s+(?P<qty>\d+)", clean_text, re.IGNORECASE)
                    if stock_match and not keywords_found:
                        ref = stock_match.group('ref').strip()
                        qty = stock_match.group('qty')
                        logger.info(f"📉 Ajuste de Stock: {ref} -> {qty}")
                        # Use shlex.quote to handle spaces/quotes correctly
                        cmd = f"update_stock --ref {shlex.quote(ref)} --qty {qty}"
                        response_text = run_manager_tool(cmd)
                        keywords_found = True

                    # COMANDO 7: TOP VENTAS
                    # "top ventas mes" / "mejores ventas año"
                    sales_match = re.search(r"(?:top|mejores|dame)\s+ventas\s+(?:del?\s+)?(?P<period>.+)", clean_text, re.IGNORECASE)
                    if sales_match and not keywords_found:
                        period = sales_match.group('period').strip()
                        logger.info(f"📊 Top Ventas: {period}")
                        cmd = f"top_sales --period {shlex.quote(period)}"
                        response_text = run_manager_tool(cmd)
                        keywords_found = True

                    # COMANDO 8: CHECK STOCK
                    # "¿tienes [X]?", "tenemos [X]?", "stock de [X]", "hay [X]?"
                    stock_check_match = re.search(r"(?:tienes|tenemos|hay|busca)\s+(?:stock\s+(?:de\s+)?)?(?P<query>.+?)\??$", clean_text, re.IGNORECASE)
                    
                    # Evitar conflictos con "añade" o "top ventas"
                    if stock_check_match and not keywords_found and "añade" not in clean_text_lower and "top" not in clean_text_lower:
                        query = stock_check_match.group('query').strip()
                        # Filtrar queries muy cortas o comunes
                        if len(query) > 2:
                            logger.info(f"🔎 Buscando stock de: {query}")
                            cmd = f"check_stock --query {shlex.quote(query)}"
                            response_text = run_manager_tool(cmd)
                            keywords_found = True

                    # DEBUGGING: Si tiene "añade" y "http" pero falló el regex
                    elif "añade" in clean_text_lower and "http" in clean_text_lower and not keywords_found:
                         response_text = (
                             "⚠️ **No reconocí el formato del comando.**\n"
                             f"Recibí esto: `{clean_text}`\n\n"
                             "Formato esperado: `añade [URL] a [PRECIO] en [CATEGORIA]`"
                         )
                         keywords_found = True
                    
                    # NUEVO: Si dice "añade" (o parecido) pero sin URL
                    elif any(x in clean_text_lower for x in ['añade', 'añadir', 'añadas', 'crear', 'nuevo', 'pon', 'mete']) and not keywords_found:
                        response_text = (
                            "🧐 **Para añadir un producto hace falta:** una **URL**, un **precio** y una **categoría** (palabra clave).\n"
                            "Ejemplo: `añade https://... a 20.00 en juegos`"
                        )
                        keywords_found = True

                    # COMANDO 6: DETECCIÓN DE URL (Educativo - Fallback)
                    elif ("http" in clean_text_lower or "www." in clean_text_lower) and not keywords_found:
                        response_text = (
                            "🔗 **Enlace detectado.**\n"
                            "Para importar: `añade [URL_PRODUCTO] a [PRECIO] en [CATEGORIA]`"
                        )
                        keywords_found = True
                    
                    # RESPUESTA DEFAULT
                    if not keywords_found and is_direct_mention:
                        response_text = f"Hola {author_name}, no entendí el mensaje. Escribe **ayuda** para ver opciones."

                    # --- ACCIÓN ---
                    if response_text:
                        # Convertir MD a HTML
                        body_html = format_response_html(response_text)
                        
                        # Nota: En Odoo 'mail.thread' es un mixin abstracto, se postea sobre el modelo real
                        target_model = msg['model']
                        target_id = msg['res_id']
                        
                        if target_model and target_id:
                            models.execute_kw(DB, uid, PASS, target_model, 'message_post', [target_id], {
                                'body': body_html,
                                'message_type': 'comment',
                                'subtype_xmlid': 'mail.mt_comment',
                                'author_id': bot_partner_id
                            })
                            logger.info(f"✅ Respondido a {author_name}.")
                        else:
                            logger.warning(f"⚠️ No se pudo responder: falta modelo/ID ({target_model}, {target_id})")
            
            # Polling con espera
            time.sleep(3)

        except KeyboardInterrupt:
            logger.info("\n🛑 Deteniendo listener...")
            break
        except Exception as e:
            logger.error(f"⚠️ Error en bucle: {e}")
            time.sleep(5)
            # Reintentar conexión
            uid, models = connect()

if __name__ == "__main__":
    listen_loop()
