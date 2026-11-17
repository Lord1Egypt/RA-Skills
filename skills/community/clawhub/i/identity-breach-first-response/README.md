# Identity Breach First Response

**The breach email says "we take security seriously." Your phone just
dropped to SOS. Those two facts are related, and the next 60 minutes
decide whether this is a password rotation or a two-year identity-theft
case.**

Data breaches hit billions of accounts; the damage is decided not by the
hack but by the first hour of response. Most people rotate the one
password they were told about and miss the three things that actually
matter: the email account that can reset everything, the session tokens
that keep an attacker logged in after a password change, and the
SIM-swap that turns your 2FA codes into his codes. When an SSN is in the
dataset, new accounts can open silently for years — a freeze stops that
in 15 minutes, if you know the mechanics.

## What it does

- **`scope`** — what leaked → what each field actually unlocks, plus the
  reuse blast-radius math (120 accounts × 25% reuse = ~30 sibling
  accounts on the stuffing list) and the verdict class.
- **`contain`** — the ordered first-60-minutes checklist with the WHY
  per step: email before banking (it resets everything), password
  manager next, revoke-sessions rule, SIM-swap carrier branch.
- **`freeze`** — SSN-in-scope credit freeze plan: all three bureaus with
  contacts, PIN handling (manager, never email), minors quirk, IRS IP
  PIN, freeze-vs-lock-vs-alert verdict table.
- **`monitor`** — the 90-day watch plan with dated checks and the
  escalate-to-report triggers.
- **`report`** — generates the FTC IdentityTheft.gov report workflow +
  FCRA §605B bureau dispute letter when fraudulent accounts appear.

## Quick start

```bash
python3 scripts/breach_response.py scope --leaked password,email,phone,ssn \
    --accounts 120 --reuse 0.25
python3 scripts/breach_response.py contain --min 60
python3 scripts/breach_response.py freeze --ssn yes
python3 scripts/breach_response.py monitor
python3 scripts/breach_response.py report --ftc-number 1234567 \
    --items "Finnacle Bank #4411 opened 2026-09-02"
```

Stdlib only, offline, no accounts. Defensive guidance only — never pay
an extortionist, and never click links in the breach notice itself.

MIT © Denis Voronin
