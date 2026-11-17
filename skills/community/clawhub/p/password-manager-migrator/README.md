# Password Manager Migrator

**The login you'll need in week 3 is the one that silently didn't import.**

People switch password managers (price, features, breakups, employers) and
discover the export formats don't map: TOTP seeds vanish on CSV hops,
attachments never ride exports, folder structures collapse, modified-dates
lie. The import tool says "success" either way. This skill plans the
migration properly — and audits it with the only method that works:
counting.

## What it does

- **`plan`** — best route per hop (10 manager pairs), what survives, what's
  LOST (with warnings on silent drops), 9 ordered steps incl. the 30-day
  read-only cutover.
- **`worksheet`** — field-mapping CSV per hop + dedupe precedence rules.
- **`totp`** — TOTP loss assessment and the re-enrollment protocol (the
  one-shot-seed problem) for CSV and native routes.
- **`audit`** — count-based verification: pass/fail verdict on pre/post
  item counts per type, with silent-drop recovery steps.

**Design constraint: zero secrets.** The scripts work from counts and
metadata you paste — no passwords, no vault files, no network.

## Quick start

```bash
python3 scripts/vault_migrate.py plan --src bitwarden --dst 1password
python3 scripts/vault_migrate.py totp --via csv
python3 scripts/vault_migrate.py audit --pre-logins 412 --post-logins 398 \
  --pre-notes 55 --post-notes 55 --pre-cards 9 --post-cards 9 \
  --duplicates 41 --weak-left 23
```

Stdlib-only Python 3. Offline.

## Layout

- `SKILL.md` — triggers, route matrix summary, traps, pitfalls
- `references/route-matrix.md` — export menu paths per manager, hop
  details, encrypted-export options, importer quirks, cutover plan
- `references/audit-worksheet.md` — count tables, silent-drop hunting,
  dedupe rules, TOTP protocol, merge workflow
- `scripts/vault_migrate.py` — the planner

## License

MIT © Denis Voronin
