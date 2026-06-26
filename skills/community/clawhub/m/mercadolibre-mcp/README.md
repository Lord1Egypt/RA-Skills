# @traid/mercadolibre-mcp

MCP server completo para Mercado Libre. 11 tools de operaciones de seller para usar desde Claude Code, Cursor, o cualquier cliente MCP.

## Tools disponibles

| Tool | Descripción | Tipo |
|------|-------------|------|
| `list_products` | Lista productos/publicaciones de un vendedor | Lectura |
| `get_orders` | Obtiene órdenes/ventas con detalle | Lectura |
| `update_price` | Actualiza precio de una publicación | Escritura |
| `update_stock` | Actualiza stock de una publicación | Escritura |
| `list_questions` | Lista preguntas recibidas | Lectura |
| `answer_question` | Responde una pregunta | Escritura |
| `get_item_metrics` | Métricas: visitas, conversión, salud | Lectura |
| `manage_ads` | Gestiona Product Ads (activar/pausar/status) | Escritura |
| `get_reputation` | Reputación del vendedor | Lectura |
| `search_competitors` | Busca productos de la competencia | Lectura |
| `get_categories` | Categorías y atributos para publicar | Lectura |

## Setup

Dos modos de autenticación:

### Opción A: Token directo (recomendado si tenés n8n/cron renovando el token)

```json
{
  "mcpServers": {
    "mercadolibre": {
      "command": "node",
      "args": ["path/to/mercadolibre-mcp/dist/index.js"],
      "env": {
        "ML_ACCESS_TOKEN": "APP_USR-...",
        "ML_SITE_ID": "MLA"
      }
    }
  }
}
```

### Opción B: Auto-refresh (standalone, sin dependencias externas)

1. Ir a [developers.mercadolibre.com](https://developers.mercadolibre.com)
2. Crear aplicación → obtener `CLIENT_ID` y `CLIENT_SECRET`
3. Autorizar vía OAuth → obtener `REFRESH_TOKEN`

```json
{
  "mcpServers": {
    "mercadolibre": {
      "command": "node",
      "args": ["path/to/mercadolibre-mcp/dist/index.js"],
      "env": {
        "ML_CLIENT_ID": "tu_client_id",
        "ML_CLIENT_SECRET": "tu_client_secret",
        "ML_REFRESH_TOKEN": "tu_refresh_token",
        "ML_SITE_ID": "MLA"
      }
    }
  }
}
```

### 3. Sites soportados

| Site ID | País |
|---------|------|
| MLA | Argentina |
| MLU | Uruguay |
| MLB | Brasil |
| MLC | Chile |
| MLM | México |
| MCO | Colombia |

## Uso

Una vez configurado, Claude Code puede ejecutar directamente:

- "Listame los productos activos"
- "Mostrá las órdenes de hoy"
- "Actualizá el precio de MLA123456 a $5000"
- "Qué preguntas sin responder tengo?"
- "Buscá competencia para repuestos de freno Toyota"

## Características

- **OAuth2 auto-refresh**: El token se renueva automáticamente cada 6h
- **Rate limiting**: Retry automático con backoff ante límites de la API
- **Multi-get batching**: Consultas de múltiples items en lotes de 20
- **Errores en español**: Mensajes de error claros, no JSON crudo
- **Sin cache**: Datos siempre en tiempo real
- **Validación Zod**: Cada parámetro validado antes de llamar a la API

## Desarrollo

```bash
cd mcp-servers/mercadolibre
npm install
npm run build    # Compilar TypeScript
npm run dev      # Desarrollo con tsx
```

## Licencia

MIT
