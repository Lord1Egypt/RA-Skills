---
name: email-reader
version: "2.0.0"
description: >
  Reads emails from Gmail (all folders/labels) using the gog CLI.
  Use when the user asks to check email, read inbox, show unread messages,
  list folders, search messages, or fetch emails from any Gmail label.
homepage: https://gogcli.sh
metadata:
  clawdbot:
    emoji: "📥"
    requires:
      bins: ["gog"]
      env:
        - name: GOG_ACCOUNT
          description: "Tu dirección de Gmail, ej: tu@gmail.com"
    install:
      - id: brew
        kind: brew
        formula: steipete/tap/gogcli
        bins: ["gog"]
        label: "Install gog CLI (brew)"
---

# Email Reader

Lee correos de Gmail usando el CLI `gog`. Requiere que `gog auth` esté
configurado. Si no lo está, ejecuta el setup primero.

## Setup inicial (solo una vez)

```bash
gog auth credentials /ruta/a/client_secret.json
gog auth add $GOG_ACCOUNT --services gmail
gog auth list   # verificar que quedó bien
```

## Cuándo usar esta skill

- "Revisa mi correo"
- "¿Qué correos nuevos tengo?"
- "Muéstrame los no leídos de hoy"
- "Lee los correos de Juan"
- "Busca correos sobre la propuesta del Q1"
- "¿Cuántos correos de spam tengo?"
- "Muéstrame el hilo de [asunto]"
- "Lee la carpeta Clientes"

## Comandos principales

### Leer inbox (correos recientes)
```bash
gog gmail search 'in:inbox newer_than:1d' --max 20 --json
gog gmail search 'in:inbox is:unread' --max 50 --json
gog gmail search 'in:inbox newer_than:7d' --max 100 --json
```

### Leer spam
```bash
gog gmail search 'in:spam newer_than:30d' --max 50 --json
```

### Leer una carpeta/etiqueta específica
```bash
# Etiquetas de sistema
gog gmail search 'in:sent newer_than:7d' --max 20 --json
gog gmail search 'in:drafts' --max 20 --json
gog gmail search 'in:trash newer_than:30d' --max 20 --json
gog gmail search 'is:starred' --max 20 --json

# Etiquetas personalizadas (carpetas del usuario)
gog gmail search 'label:Clientes newer_than:30d' --max 20 --json
gog gmail search 'label:Proyectos' --max 20 --json
gog gmail search 'label:Facturas newer_than:90d' --max 20 --json
```

### Buscar correos
```bash
# Por remitente
gog gmail search 'from:juan@empresa.com newer_than:30d' --max 20 --json

# Por asunto
gog gmail search 'subject:propuesta' --max 10 --json

# Por contenido
gog gmail search 'propuesta presupuesto 2026' --max 10 --json

# Combinado
gog gmail search 'from:ceo@empresa.com is:unread newer_than:7d' --max 10 --json

# Con adjuntos
gog gmail search 'has:attachment in:inbox newer_than:7d' --max 10 --json
```

### Filtros de tiempo útiles
| Filtro | Significado |
|--------|-------------|
| `newer_than:1d` | último día |
| `newer_than:7d` | última semana |
| `newer_than:30d` | último mes |
| `older_than:180d` | más de 6 meses |
| `after:2026/01/01` | desde fecha exacta |

## Presentación de resultados

Después de obtener el JSON, presenta un resumen claro al usuario:

```
📥 INBOX — 8 correos nuevos (3 no leídos)

  ⭐ [hoy 09:14] ceo@empresa.com
     "Reunión urgente esta tarde"

  📧 [hoy 08:30] juan@empresa.com
     "Re: Propuesta Q1 2026"

  📰 [ayer 18:00] newsletter@medium.com
     "Top 10 AI tools this week"
  ...

¿Quieres que analice estos correos o que responda alguno?
```

## Múltiples cuentas

Si el usuario tiene más de una cuenta de Gmail:
```bash
# Listar cuentas configuradas
gog auth list

# Leer de una cuenta específica
gog gmail search 'in:inbox is:unread' --account otra@gmail.com --max 20 --json

# Cambiar cuenta por defecto
export GOG_ACCOUNT=otra@gmail.com
```

## Notas importantes
- Usar siempre `--json` para obtener datos estructurados
- Usar `--no-input` en modo automático/cron para evitar prompts interactivos
- El flag `--max` limita resultados; aumentar si el usuario quiere más
- Los resultados de búsqueda de Gmail usan la misma sintaxis que gmail.com
