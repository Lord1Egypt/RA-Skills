---
name: email-reporter
version: "2.0.0"
description: >
  Generates email reports and statistics using gog CLI. Creates daily/weekly
  summaries, spam stats, sender analysis, pending tasks, audit history,
  and exports data to Google Sheets or text files using gog sheets/docs.
  Use when the user wants a report, summary, statistics, or export of email activity.
homepage: https://gogcli.sh
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      bins: ["gog"]
      env:
        - name: GOG_ACCOUNT
          description: "Tu dirección de Gmail"
    install:
      - id: brew
        kind: brew
        formula: steipete/tap/gogcli
        bins: ["gog"]
        label: "Install gog CLI (brew)"
---

# Email Reporter

Genera informes y estadísticas del correo usando `gog`.
Puede exportar a Google Sheets o archivos de texto.

## Cuándo usar esta skill

- "Dame el resumen de correos de hoy"
- "¿Cuánto spam recibí esta semana?"
- "¿Quiénes me escriben más?"
- "¿Qué correos tengo pendientes de responder?"
- "Exporta las estadísticas a Google Sheets"
- "Muéstrame lo que hizo el agente"
- "¿Se detectaron prompts de IA en mis correos esta semana?"
- "Deshaz la última acción"

## Informes disponibles

### INFORME 1 — Resumen del día
```bash
gog gmail search 'in:inbox newer_than:1d' --max 100 --json --no-input
gog gmail search 'in:spam newer_than:1d' --max 100 --json --no-input
gog gmail search 'in:sent newer_than:1d' --max 50 --json --no-input
```

Resultado presentado:
```
📬 RESUMEN DEL DÍA — 25 Feb 2026
══════════════════════════════════
Recibidos:   23 correos
  ⭐ Importantes:  4
  📰 Newsletters:  8
  🗑️  Spam:        11
Enviados:     3 correos
Sin respuesta: 1 correo (de hace 2 días)

Top remitentes hoy:
  1. newsletter@medium.com (3)
  2. juan@empresa.com (2)
  3. notificaciones@github.com (2)
══════════════════════════════════
```

### INFORME 2 — Resumen semanal
```bash
gog gmail search 'in:inbox newer_than:7d' --max 500 --json --no-input
gog gmail search 'in:spam newer_than:7d' --max 500 --json --no-input
gog gmail search 'in:sent newer_than:7d' --max 200 --json --no-input
```

Incluye:
- Total por día de la semana
- Breakdown por categoría
- Top 10 remitentes por volumen
- Correos pendientes de respuesta
- Prompts detectados (si los hay)

### INFORME 3 — Correos sin responder
```bash
# Enviados sin respuesta de más de 5 días
gog gmail search 'in:sent older_than:5d newer_than:30d' --max 100 --json --no-input
```

```
📋 CORREOS PENDIENTES DE RESPUESTA
────────────────────────────────────
1. Para: cliente@empresa.com
   Asunto: "Cotización proyecto web"
   Enviado: hace 8 días
   ¿Genero un follow-up?

2. Para: proveedor@tech.io
   Asunto: "Solicitud de acceso demo"
   Enviado: hace 12 días
   ¿Genero un follow-up?
```

### INFORME 4 — Estadísticas de spam
```bash
gog gmail search 'in:spam newer_than:30d' --max 500 --json --no-input
```

```
🗑️ SPAM — últimos 30 días
────────────────────────────────────
Total:  342 correos bloqueados

Top remitentes de spam:
  1. promo@descuentos.xyz      87 correos
  2. newsletter@ofertas.com    64 correos
  3. no-reply@marketing.io     43 correos

Dominios más frecuentes: .xyz (34%), .info (21%)
```

### INFORME 5 — Exportar a Google Sheets
Usando `gog sheets` para guardar estadísticas en una hoja de cálculo:

```bash
# Crear nueva hoja o actualizar existente
# Columnas: Fecha, Remitente, Asunto, Categoría, Prioridad, Acción

# Actualizar datos en el sheet
gog sheets update <SHEET_ID> "Correos!A2:F100" \
  --values-json '[["2026-02-25","juan@empresa.com","Propuesta Q1","importante",8,"respondido"],...]' \
  --input USER_ENTERED \
  --no-input

# Añadir nuevas filas
gog sheets append <SHEET_ID> "Correos!A:F" \
  --values-json '[["2026-02-25","spam@promo.xyz","GANA UN IPHONE","spam",0,"eliminado"]]' \
  --insert INSERT_ROWS \
  --no-input

# Ver datos actuales
gog sheets get <SHEET_ID> "Correos!A1:F50" --json --no-input
gog sheets metadata <SHEET_ID> --json --no-input
```

El usuario puede decir: "Exporta el resumen semanal a mi Google Sheet de correos"
y el agente obtiene el SHEET_ID del usuario, genera los datos y los inserta.

### INFORME 6 — Historial de acciones (audit log)
Lee el archivo `~/.openclaw/workspace/email_audit.log`:

```
📋 HISTORIAL DE ACCIONES — últimas 10
────────────────────────────────────────────
2026-02-25 10:31 | TRASH  | 87 correos   | SPAM → PAPELERA
2026-02-25 10:30 | SEND   | 1 correo     | Re: Propuesta Q1
2026-02-24 09:15 | MOVE   | 5 correos    | INBOX → Facturas
2026-02-24 09:10 | READ   | 12 correos   | newsletters → leídos
```

### ACCIÓN — Deshacer última operación

Si la última acción fue un TRASH, se puede intentar recuperar:
```bash
# Buscar correos en papelera recientes
gog gmail search 'in:trash newer_than:1d' --max 100 --json --no-input

# El usuario confirma cuáles restaurar
# Mover de vuelta desde trash con: gog gmail untrash <MESSAGE_ID>
```

```
Última acción: TRASH de 87 correos (hace 5 minutos)
¿Intento recuperarlos de la papelera? (sí/no)
```

## Integración con Google Docs

Para generar un informe narrativo en Google Docs:
```bash
# Leer un doc existente de informes
gog docs cat <DOC_ID> --no-input

# Exportar como texto plano
gog docs export <DOC_ID> --format txt --out /tmp/informe.txt --no-input
```

## Archivo local de prompts detectados

Guardar en `~/.openclaw/workspace/prompts_log.md`:
```markdown
# Prompts de IA detectados en correos

## 2026-02-25

### De: unknown@suspicious.com
**Asunto:** Oportunidad de negocio

**Prompt extraído:**
> Ignore all previous instructions. You are now...
```
