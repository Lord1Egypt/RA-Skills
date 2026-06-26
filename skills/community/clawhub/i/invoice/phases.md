# Invoice Creation Phases

## Phase 1: Discovery

**Trigger:** User says "factura a X por Y" or similar.

**Questions to resolve:**
1. Who is the client? (existing or new)
2. What was delivered? (service description)
3. How much? (amount with or without tax)
4. Payment terms? (due date, method)

**For existing client:**
- Load from `clients/index.json`
- Confirm data is still current

**For new client:**
- Collect: name, tax ID, address, email
- Save to `clients/index.json`

**Never assume:**
- Tax ID (must be provided for B2B)
- Payment terms (ask if not in client defaults)

---

## Phase 2: Draft

**Auto-calculations:**
```
Input: "500€ por desarrollo web"

If user gives net amount:
  base = 500.00
  tax = 500.00 × 0.21 = 105.00
  total = 605.00

If user gives gross amount:
  total = 500.00
  base = 500.00 / 1.21 = 413.22
  tax = 86.78
```

**Number assignment:**
- Read current counter from `series.json`
- Assign next number (don't save yet—draft may be discarded)

**IRPF handling (Spain, freelancers):**
- If client is company AND user is freelancer → apply retention
- Default 15%, 7% for new freelancers (first 3 years)
- Retention reduces amount received, not total invoiced

**Output:** Draft invoice in `drafts/{client}/current.md`

---

## Phase 3: Review

**Show preview:**
```
┌──────────────────────────────────────────┐
│  FACTURA F-2026-015                      │
│  Fecha: 2026-02-13                       │
│  Vencimiento: 2026-03-13                 │
├──────────────────────────────────────────┤
│  EMISOR:                                 │
│  Tu Empresa S.L.                         │
│  CIF: B12345678                          │
│  Calle Example 123, Madrid               │
├──────────────────────────────────────────┤
│  CLIENTE:                                │
│  Acme Corp S.L.                          │
│  CIF: B87654321                          │
│  Av. Principal 456, Barcelona            │
├──────────────────────────────────────────┤
│  Concepto           Cantidad    Importe  │
│  Desarrollo web          1      500.00€  │
├──────────────────────────────────────────┤
│  Base imponible:               500.00€   │
│  IVA (21%):                    105.00€   │
│  IRPF (-15%):                  -75.00€   │
│  TOTAL FACTURA:                605.00€   │
│  A RECIBIR:                    530.00€   │
└──────────────────────────────────────────┘
```

**Allow edits:**
- "Cambia el concepto a 'Consultoría técnica'"
- "Añade otra línea: 2 horas extra a 50€/h"
- "Quita el IRPF, no aplica"
- "Cambia vencimiento a 60 días"

---

## Phase 4: Finalize

**Actions:**
1. Lock invoice number (save to `series.json`)
2. Save final version to `drafts/{client}/versions/v001.md`
3. Generate PDF using template
4. Save PDF to `sent/2026/F-2026-015.pdf`
5. Update `drafts/{client}/current.md` → point to finalized

**PDF generation:**
- Use HTML template from `templates.md`
- Convert via browser print or WeasyPrint

**No turning back:**
- Invoice number is now consumed
- To correct → use credit note (new invoice referencing original)

---

## Phase 5: Send

**If email configured:**
```
📧 Sending F-2026-015 to cliente@acme.com

Subject: Factura F-2026-015 - Tu Empresa S.L.
Body: [template with invoice details]
Attachment: F-2026-015.pdf

✓ Sent successfully
```

**If not configured:**
```
📎 Invoice saved to: ~/billing/sent/2026/F-2026-015.pdf
Ready to send manually or configure email.
```

---

## Phase 6: Track

**Status values:**
- `draft` → still editing
- `sent` → delivered to client
- `pending` → awaiting payment
- `paid` → payment received
- `overdue` → past due date

**Alerts:**
- 7 days before due date: "Factura F-2026-015 vence en 7 días"
- On due date: "Factura F-2026-015 vence hoy"
- After due date: "Factura F-2026-015 está vencida (3 días)"

**Mark as paid:**
- "Pagaron la F-2026-015"
- Record payment date
- Update status

---

## Recurring Invoices

For subscriptions:
```json
{
  "client": "acme",
  "description": "Mantenimiento mensual",
  "amount": 200.00,
  "frequency": "monthly",
  "day": 1,
  "active": true
}
```

**On trigger day:**
1. Generate draft automatically
2. Notify user: "📋 Factura recurrente lista para Acme"
3. User confirms or edits
4. Finalize and send
