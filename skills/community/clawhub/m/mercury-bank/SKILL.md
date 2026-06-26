---
name: mercury
description: Mercury bank API for Digital 4 Jesus LLC (US entity). Use when the user asks about Mercury account balances, transactions, invoices, customers, or sending money. Triggers on phrases like "Mercury balance", "create invoice", "check Mercury", "list invoices", "create customer", "who owes me", "send money via Mercury", "Mercury statement", or any D4J LLC banking or AR question. Requires Mercury Plus for invoicing/customer endpoints. Credentials at ~/.secrets/mercury.env.
license: MIT
---

# Mercury Skill

Mercury US business banking API for Digital 4 Jesus LLC (EIN 30-1413169).

## Setup

Credentials at `~/.secrets/mercury.env`:
```
MERCURY_API_TOKEN=secret-token:...
MERCURY_API_BASE=https://api.mercury.com/api/v1
MERCURY_AR_BASE=https://api.mercury.com/api/v1/ar
MERCURY_ORG_ID=24ff8f74-e019-11f0-9f3c-3b30f2dfe1ae
```

Auth: Basic Auth — token as username, empty password.

## Quick Commands

```bash
# Balance check
bash /root/clawd/skills/mercury/scripts/mercury.sh balance

# List invoices
bash /root/clawd/skills/mercury/scripts/mercury.sh invoices

# List customers
bash /root/clawd/skills/mercury/scripts/mercury.sh customers

# Create invoice (amount in cents — $500 = 50000)
bash /root/clawd/skills/mercury/scripts/mercury.sh create-invoice \
  <customer_id> 50000 2026-03-26 "Description" "INV-7"

# Recent transactions
bash /root/clawd/skills/mercury/scripts/mercury.sh transactions
```

## Key Account IDs

- Checking ••3223: `4ca92254-e020-11f0-ab61-779167c16d40`
- Savings ••4179: `4cd596f4-e020-11f0-ab61-4b868ee3a466`

## Known Customers

| Name | ID |
|------|----|
| Digital 4 Jesus (Pty) Ltd | b70764bc-e6e7-11f0-b2c4-f7e8b0b59579 |
| Tucbox Solutions LLC (Gareth) | b0a9dd9e-fcdf-11f0-9629-5f9339c3a927 |
| Engel Schmidt / Sentralis Inc | f8badce2-2218-11f1-b827-dfd253723134 |

## Important Notes

- **Amount is in cents**: $500 = `50000`, $250 = `25000`
- **AR endpoints require Mercury Plus** (`/ar/invoices`, `/ar/customers`)
- **Invoice numbers** auto-increment if not specified (script handles this)
- **ACH only** for US clients to avoid Stripe fees; credit card can be enabled per invoice
- For full endpoint reference, see `references/api.md`
