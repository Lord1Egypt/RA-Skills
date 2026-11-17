# password-auditor 🔐

**Audit your password habits without ever storing or transmitting a password.**

You know you're supposed to audit your passwords. You also know exporting your
vault feels risky and every online "password strength checker" means pasting
your actual password into a stranger's web form. `password-auditor` solves both
problems: it analyzes a vault export you already control, entirely offline
(except an optional breach check that only ever sends 5 characters of a hash),
and its outputs contain **zero plaintext passwords**.

## The real-world problem

- **81% of account takeovers start with reused or weak passwords.** When any
  site you use gets breached, attackers try those credentials everywhere
  (credential stuffing) — one leak becomes ten compromised accounts.
- Most people have 80-200 vault entries and no idea which ones are weak,
  reused, ancient, or already pwned.
- Password managers tell you a "health score" but not *what to fix first* or
  *how much each fix matters* (a reused bank password ≠ a reused forum password).

## What it does

Point it at a CSV/JSON export from Bitwarden, 1Password, KeePass, Chrome, or
Firefox (auto-detected). You get:

- **0-100 security score** with per-dimension sub-scores
- **Reuse analysis** — finds every group of accounts sharing one password
- **Weakness scoring** — zxcvbn-style entropy estimation (leetspeak, keyboard
  patterns, common lists — `Tr0ub4dor&3` correctly scores weak)
- **Staleness** — passwords unchanged for 4+ years
- **Breach check** (optional) — HaveIBeenPwned k-anonymity API: only the first
  5 hex chars of a SHA-1 hash leave your machine; the server sees ~800
  candidates and cannot know which is yours
- **2FA gaps** — sites that support TOTP where you haven't enrolled
- **Prioritized remediation plan** — critical sites (email, banking, SSO)
  weighted 3x, so you fix the dangerous stuff first
- **HTML dashboard + JSON** for tracking improvement over time
  (`--compare old.json new.json`)

## Quick start

```bash
# Try it safely on the built-in demo vault
python3 scripts/password_auditor.py --demo --html dashboard.html

# Audit your real export (offline analysis)
python3 scripts/password_auditor.py --vault ~/bitwarden_export.csv

# With breach exposure check
python3 scripts/password_auditor.py --vault export.csv --check-breaches

# Track improvement between audits
python3 scripts/password_auditor.py --compare audit_may.json audit_aug.json
```

## Privacy guarantees

| What | Where it goes |
|---|---|
| Vault file | Read locally, never uploaded |
| Reports (JSON/HTML) | Titles + findings only, no passwords |
| Breach check | 5-char SHA-1 prefix per password (k-anonymity) |
| Telemetry | None — the script makes zero requests without `--check-breaches` |

## Install as a skill

Copy this directory into your agent's skills folder. The agent can then run
audits whenever you ask "how bad are my passwords?" — see `SKILL.md`.

## License

MIT © Denis Voronin
