# MedPilot Self-Use Quickstart

## CLI examples

### Parse a doctor order
```bash
npm run dev -- ingest-order --patient <patient-id> --text "氯沙坦钾片 50mg，每天早饭后 1 次，每次 1 片" --base-dir .
```

### Record a metric
```bash
npm run dev -- record-metric --patient <patient-id> --type blood_pressure --values '{"systolic":168,"diastolic":102,"symptom":"头痛"}' --unit mmHg --base-dir .
```

### Build a report
```bash
npm run dev -- build-report --patient <patient-id> --base-dir .
```

## API examples

### Create patient
```bash
curl -X POST http://localhost:3456/api/patients -H 'Content-Type: application/json' -d '{"displayName":"Demo User"}'
```

### Ingest order
```bash
curl -X POST http://localhost:3456/api/orders   -H 'Content-Type: application/json'   -H 'X-MedPilot-Token: <token>'   -d '{"patientId":"<patient-id>","text":"氯沙坦钾片 50mg，每天早饭后 1 次，每次 1 片"}'
```

### Record intake
```bash
curl -X POST http://localhost:3456/api/intakes   -H 'Content-Type: application/json'   -H 'X-MedPilot-Token: <token>'   -d '{"patientId":"<patient-id>","medicationId":"<med-id>","plannedTime":"2026-03-15T08:30:00+08:00","actualTime":"2026-03-15T08:35:00+08:00"}'
```

### Build report
```bash
curl -H 'X-MedPilot-Token: <token>' "http://localhost:3456/api/patients/<patient-id>/report?startDate=2026-03-15&endDate=2026-03-21"
```

## Scope reminders
- Single-patient self-use only.
- Use generated alerts as prompts for follow-up, not diagnosis.
