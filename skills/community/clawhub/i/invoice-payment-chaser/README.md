# 💰 Invoice & Payment Chaser — OpenClaw Skill

Chase overdue invoices automatically via email and WhatsApp. Connects to Xero and
QuickBooks, sends escalating chase sequences, calculates statutory interest, generates
aged debtor reports, and stops the moment payment lands.

UK Late Payment of Commercial Debts Act 1998 compliance built in.

## What it does

- **Monitors overdue invoices** — syncs with Xero and/or QuickBooks in real time. Detects newly overdue invoices and payments received automatically
- **Sends chase sequences** — 4-stage escalating sequence: friendly reminder → follow-up → formal notice (with statutory interest) → final demand
- **WhatsApp escalation** — for high-value invoices (configurable threshold), sends a WhatsApp alert alongside Stage 3 and 4 emails
- **Statutory interest** — calculates and includes Late Payment Act interest (8% + BoE base rate) in Stage 3/4 emails automatically
- **Aged debtor reports** — full breakdown by client and age band, with collection rate tracking
- **Dispute management** — pause chasing for disputed invoices, add notes, resume or write off
- **Payment detection** — instantly notified when a payment is received during a sync
- **Never chases on weekends** — queues weekend emails for Monday automatically

## Example usage

```
You:  check overdue invoices
Bot:  💰 £8,340 outstanding across 6 invoices
      🔴 Apex Design £2,400 — 74 days — final demand
      🟠 Blue Wave Agency £1,850 — 38 days — Stage 3 due
      🟡 Metro Retail £2,100 — 12 days — Stage 2 due
      Reply "send all due" to chase today

You:  send all due
Bot:  📧 5 chase emails ready — total £5,940
      Stage 3 emails include statutory interest (£25.15 total)
      Send all? YES / review each / skip

You:  yes
Bot:  ✅ 5 chases sent — £5,940 pursued
      Next: Apex Design final demand awaits your approval
```

## Who it's for

Any UK business that invoices clients — freelancers, agencies, consultants,
tradespeople, and service businesses. Not limited to product sellers.

## Integrations

- **Xero** — full invoice read/update, contact details, payment recording
- **QuickBooks Online** — full invoice read, contact details
- **Email** — SMTP/IMAP (Gmail app password or any provider)
- **WhatsApp** — via OpenClaw's configured channel (for high-value escalations)

## UK law

- Late Payment of Commercial Debts (Interest) Act 1998 — 8% + BoE base rate
- Late Payment of Commercial Debts Regulations 2013 — fixed recovery costs (£40/£70/£100)
- Stage 4 final demand mentions CCJ and debt collection options
- This skill provides information, not legal advice

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | 7 workflows, chase templates for all 4 stages, statutory interest calculation, dispute management |
| `EXAMPLES.md` | 9 examples covering check, send, Stage 1–4 emails, payment received, dispute, reports |
| `CONFIG.md` | Xero and QuickBooks OAuth setup, email config, troubleshooting |

## Notes

- Stage 4 (final demand) always requires owner approval — never auto-sent
- Chases are never sent on Saturdays, Sundays, or UK bank holidays
- Statutory interest only applies to B2B transactions — the skill notes this
- Token refresh happens automatically — re-auth only needed every 60 days of inactivity
