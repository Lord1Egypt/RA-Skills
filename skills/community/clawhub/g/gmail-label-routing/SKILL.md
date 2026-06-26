---
name: gmail-label-routing
description: Configurar en Gmail el enrutamiento por remitente hacia etiquetas usando el workflow local `scripts/gws_gmail_label_workflow.py`, incluyendo crear/usar etiqueta, crear filtro, aplicar retroactivo y opcionalmente sacar de INBOX. Usar cuando el usuario pida cosas como “manda este remitente a esta etiqueta”, “hazlo para varios remitentes”, “aplícalo a correos existentes”, “sácalos de INBOX”, o “limpia/reemplaza filtros duplicados para ese remitente”.
---

# Gmail Label Routing

## Overview

Estandarizar cambios de etiquetas por remitente en Gmail con un flujo único y consistente.
Priorizar el script local para evitar inconsistencias manuales entre filtro, retroaplicación y estado de INBOX.

## Workflow

1. Confirmar intención del usuario:
- Etiqueta destino
- Uno o varios remitentes
- Si debe salir de INBOX (default: sí)
- Si debe reemplazar filtros existentes del remitente (solo cuando lo pida o haya conflictos)

2. Ejecutar el workflow:

```bash
python3 scripts/gws_gmail_label_workflow.py \
  --label "<Etiqueta>" \
  --sender "correo1@dominio.com" \
  --sender "correo2@dominio.com"
```

> `scripts/gws_gmail_label_workflow.py` es ruta relativa al directorio de esta skill.

3. Variantes comunes:
- Mantener en INBOX: `--keep-inbox`
- Reemplazar filtros del remitente: `--replace-sender-filters`
- Simular sin cambios: `--dry-run`

4. Confirmar resultado con el JSON final del script:
- `createdFilterId`
- `retroApplied`
- `withLabelCount`
- `inboxCount`

## Rules

- Repetir `--sender` por cada remitente.
- Mantener comillas en etiqueta y remitentes para evitar errores de parsing.
- Usar `--replace-sender-filters` cuando haya mezcla por reglas duplicadas para el mismo remitente.
- Si el usuario dice “haz lo mismo”, repetir el mismo patrón usado: etiqueta + filtro + retroactivo + manejo de INBOX.
- Si hay fallo de scopes en `gws` para filtros, usar el fallback ya implementado dentro del workflow (credenciales OAuth locales).

## Reference

- Ver ejemplos listos en `references/commands.md`.
