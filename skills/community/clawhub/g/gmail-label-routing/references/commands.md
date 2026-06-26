# Command Examples

## 1) Un remitente a una etiqueta (y fuera de INBOX)

```bash
python3 scripts/gws_gmail_label_workflow.py \
  --label "FIUSAC" \
  --sender "noreply@ingenieria.usac.edu.gt"
```

## 2) Varios remitentes a una etiqueta

```bash
python3 scripts/gws_gmail_label_workflow.py \
  --label "Notificaciones bancarias" \
  --sender "informacion@ventaspromerica.com.gt" \
  --sender "info@info.baccredomatic.net"
```

## 3) Mantener en INBOX

```bash
python3 scripts/gws_gmail_label_workflow.py \
  --label "Polymarket" \
  --sender "noreply@polymarket.com" \
  --keep-inbox
```

## 4) Reemplazar filtros duplicados/conflictivos

```bash
python3 scripts/gws_gmail_label_workflow.py \
  --label "TC/BAC" \
  --sender "EstadodeCuentaBAC@baccredomatic.gt" \
  --replace-sender-filters
```

## 5) Dry run

```bash
python3 scripts/gws_gmail_label_workflow.py \
  --label "IA News" \
  --sender "noreply@mail.societyai.com" \
  --dry-run
```
