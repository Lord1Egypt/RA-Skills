---
name: email-reader
description: Read/search Gmail via gog CLI (preferred) or Python scripts (fallback). Inbox check, email search, content retrieval, IMAP support.
metadata:
  clawdbot:
    emoji: "📬"
    requires:
      bins: ["gog"]
      env:
        - name: GOG_ACCOUNT
          description: "Tu dirección Gmail, ej: tu@gmail.com"
        - name: GMAIL_CREDENTIALS_PATH
          description: "(Solo Python) Ruta a credentials.json"
    install:
      - id: brew
        kind: brew
        formula: steipete/tap/gogcli
        bins: ["gog"]
        label: "Install gog CLI (brew)"
    routing:
      recommended: "google/gemini-2.5-flash-lite"
      alternatives: ["openrouter/google/gemini-2.5-flash-lite", "openai/gpt-4o-mini"]
      reason: "Read-only, low reasoning. Cheapest model sufficient."
---

# email-reader

## Cuándo usar
Usuario pide revisar inbox, buscar correos, leer mensajes, listar carpetas, o ver emails recientes.

## Backend A — gog CLI (preferido)

### Setup (una vez)
```bash
brew install steipete/tap/gogcli
gog auth credentials /ruta/credentials.json
gog auth add $GOG_ACCOUNT --services gmail
```

### Comandos
```bash
# No leídos (acción por defecto)
gog gmail search 'in:inbox is:unread' --max 5 --format minimal --json --no-input

# Búsqueda por criterio
gog gmail search '<query>' --max 10 --format minimal --json --no-input

# Correo completo
gog gmail get <ID> --format full --json --no-input

# Hilo completo
gog gmail thread <THREAD_ID> --format minimal --json --no-input
```

### Queries útiles
```bash
# Carpetas sistema
'in:inbox newer_than:1d'   'in:spam newer_than:30d'
'in:sent newer_than:7d'    'is:starred'

# Etiquetas personalizadas
'label:Clientes'  'label:Facturas newer_than:90d'

# Filtros
'from:juan@empresa.com is:unread'
'subject:propuesta newer_than:7d'
'has:attachment in:inbox newer_than:7d'
```

### Operadores Gmail
`from:` `to:` `subject:` `label:` `is:unread` `is:starred` `has:attachment`
`newer_than:Nd` `older_than:Nd` `in:inbox` `in:sent` `after:YYYY/MM/DD`

## Backend B — Python (fallback)

### Setup (una vez)
```bash
pip install google-api-python-client google-auth-oauthlib beautifulsoup4 cryptography
python3 scripts/auth.py   # OAuth → genera token.json cifrado
```

### Comandos
```bash
python3 scripts/fetch_emails.py --label INBOX --max 50
python3 scripts/fetch_emails.py --label INBOX --unread-only --max 20
python3 scripts/fetch_emails.py --label INBOX --since 2026-01-01
python3 scripts/fetch_emails.py --label INBOX --from juan@empresa.com
python3 scripts/fetch_emails.py --label SPAM  --max 100
python3 scripts/fetch_emails.py --label Clientes --max 30
python3 scripts/list_folders.py                     # listar etiquetas
python3 scripts/fetch_thread.py --thread-id <ID>   # hilo completo
python3 scripts/imap_fetch.py --host imap.outlook.com --folder INBOX  # no-Gmail
```

## Flujo
1. Detectar backend: `command -v gog &>/dev/null && BACKEND=gog || BACKEND=python`
2. Construir query desde intent del usuario — preguntar si ambiguo
3. Ejecutar con `--max N` conservador (default 5-10)
4. Parsear JSON → presentar: remitente, asunto, fecha, preview + ID
5. Ofrecer: leer completo, refinar búsqueda, actuar

## Reglas
- SIEMPRE `--json` + `--no-input`; nunca mostrar JSON crudo
- Default `--max 5`; subir solo si usuario pide más
- Preservar IDs para acciones posteriores
- Sin resultados → sugerir query más amplio
- Solo lectura; enviar/responder → **email-responder**

## Errores
- `gog` missing → `brew install steipete/tap/gogcli`
- `GOG_ACCOUNT` unset → pedir Gmail al usuario
- Token expired → `gog auth add <email>` / `python3 scripts/auth.py`
