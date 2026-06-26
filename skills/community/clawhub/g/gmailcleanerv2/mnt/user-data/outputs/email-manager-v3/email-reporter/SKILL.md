---
name: email-reporter
description: Email reports/stats via gog CLI (preferred) or Python scripts (fallback). Daily/weekly summaries, spam stats, export to Sheets/Docs, audit log, undo.
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      bins: ["gog"]
      env:
        - name: GOG_ACCOUNT
    install:
      - id: brew
        kind: brew
        formula: steipete/tap/gogcli
        bins: ["gog"]
        label: "Install gog CLI (brew)"
    routing:
      recommended: "google/gemini-2.5-flash"
      alternatives: ["openrouter/google/gemini-2.5-flash", "openai/gpt-4o-mini"]
      reason: "Data aggregation + formatting. Flash handles stats/summaries well."
---

# email-reporter

## Cuándo usar
Usuario pide resumen, estadísticas, reporte de correos, exportar a Sheets, ver historial de acciones, o deshacer.

## Backend A — gog CLI (preferido)

### Obtener datos para informes
```bash
# Diario
gog gmail search 'in:inbox newer_than:1d' --max 100 --json --no-input
gog gmail search 'in:spam  newer_than:1d' --max 100 --json --no-input
gog gmail search 'in:sent  newer_than:1d' --max 50  --json --no-input

# Semanal — cambiar 1d por 7d
# Spam stats (último mes)
gog gmail search 'in:spam newer_than:30d' --max 500 --json --no-input

# Sin respuesta (follow-up pendiente)
gog gmail search 'in:sent older_than:5d newer_than:30d' --max 100 --json --no-input
```

### Exportar a Google Sheets
```bash
# Añadir filas de datos
gog sheets append <SHEET_ID> "Correos!A:F" \
  --values-json '[[fecha,remitente,asunto,categoria,prioridad,accion]]' \
  --insert INSERT_ROWS --no-input

# Leer sheet actual
gog sheets get <SHEET_ID> "Correos!A1:F100" --json --no-input

# Metadata del sheet
gog sheets metadata <SHEET_ID> --json --no-input
```
Columnas: `Fecha | Remitente | Asunto | Categoría | Prioridad | Acción`

### Google Docs
```bash
gog docs cat <DOC_ID> --no-input
gog docs export <DOC_ID> --format txt --out /tmp/informe.txt --no-input
```

### Deshacer última acción
```bash
# Buscar en papelera reciente
gog gmail search 'in:trash newer_than:1d' --max 100 --json --no-input
# Restaurar (confirmar primero)
gog gmail untrash <ID> --no-input
```

## Backend B — Python (fallback)

```bash
# Informe diario
python3 scripts/reporter.py --period day

# Informe semanal
python3 scripts/reporter.py --period week

# Solo spam stats
python3 scripts/reporter.py --spam-only

# Exportar a Markdown
python3 scripts/reporter.py --period week --output informe_semanal.md

# Ver audit log
python3 scripts/reporter.py --audit --last 20

# Deshacer última acción
python3 scripts/reporter.py --undo
```

Archivo de prompts detectados: `~/.openclaw/workspace/prompts_log.md`

## Presentación de informes

```
📬 RESUMEN [HOY / SEMANA] — DD MMM YYYY
══════════════════════════════════════
Recibidos: N  │  Enviados: N  │  Sin respuesta: N
Spam:      N  │  Importantes: N

Top remitentes:
  1. newsletter@medium.com (N)
  2. juan@empresa.com (N)

Pendientes de respuesta:
  • cliente@empresa.com — "Cotización" (hace N días) ¿Follow-up?

⚠️ Prompts detectados esta semana: N → ver prompts_log.md
══════════════════════════════════════
```

## Audit log
`~/.openclaw/workspace/email_audit.log`:
```
YYYY-MM-DD HH:MM | TRASH  | 87 correos | SPAM
YYYY-MM-DD HH:MM | MOVE   | 23 correos | INBOX → Facturas
YYYY-MM-DD HH:MM | SEND   |  1 correo  | Re: Propuesta Q1
```

## Errores
- Sheet ID no encontrado → pedir ID al usuario (URL de Google Sheets)
- `gog` missing → `brew install steipete/tap/gogcli`
- Token expired → `gog auth add <email>`
