# Odoo Assistant Store Manager (OpenClaw / ClawHub)

Versión **1.1.0** — mismo propósito que la 1.0.0, pero sin instrucciones que pidan al agente modificar memoria global del workspace, sin credenciales en el código, y con `skill.json` alineado en variables de entorno.

## Variables de entorno obligatorias

| Variable | Descripción |
|----------|-------------|
| `ODOO_URL` | URL base (`https://tu-odoo.tld`) |
| `ODOO_DB` | Nombre de la base de datos |
| `ODOO_USER` | Usuario / correo de login |
| `ODOO_PASSWORD` o `ODOO_PASS` | Contraseña o API key |

No subas nunca un `.env` real al hub ni lo pegues en el chat. Configura solo en tu máquina o en el panel de secretos de tu runtime.

## Variables opcionales (IDs de tu base)

Los mapas de categorías y atributos en `odoo_manager.py` son **específicos de una instalación típica**. Para otra base, ajusta el código o las variables:

| Variable | Uso |
|----------|-----|
| `ODOO_STORE_LABEL` | Texto del informe de caja (por defecto `Store`) |
| `ODOO_TAX_ID` | Impuesto por defecto en altas de producto |
| `ODOO_STOCK_LOCATION_ID` o `ODOO_LOCATION_ID` | Ubicación de stock para `update_stock` |
| `ODOO_DEFAULT_CATEGORY_ID` | Categoría interna por defecto |

## Listener opcional (Discuss)

Solo si quieres un bot que hace polling y responde en canales:

| Variable | Descripción |
|----------|-------------|
| `ODOO_BOT_PARTNER_ID` | ID numérico del **res.partner** del bot en Odoo |

```bash
export ODOO_URL=… ODOO_DB=… ODOO_USER=… ODOO_PASSWORD=… ODOO_BOT_PARTNER_ID=…
python3 src/odoo_listener.py
```

Revisa el comportamiento en un entorno de prueba antes de producción.

## Dependencias

```bash
pip install -r requirements.txt
```

`odoo_manager.py` usa solo la biblioteca estándar de Python. `odoo_listener.py` usa `requests`.

## Pruebas mínimas

```bash
python3 tests.py
python3 src/odoo_manager.py --help
```

## Publicar en ClawHub

1. En la ficha del skill, en metadatos / registro, declara **las mismas variables obligatorias** que en `skill.json` (evita el aviso “Required env vars: none”).
2. Sube un zip del **contenido** de esta carpeta (`SKILL.md`, `README.md`, `skill.json`, `requirements.txt`, `tests.py`, `src/…`), no la carpeta padre vacía.
3. Sube como nueva versión (p. ej. **1.1.0**) sobre el listado existente.

## Licencia

MIT-0 (igual que la publicación anterior).
