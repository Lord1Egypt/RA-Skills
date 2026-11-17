---
name: password-manager-migrator
description: Use when moving between password managers (Bitwarden/1Password/Keepass/Apple/Chrome/Proton), merging vaults, or auditing one — builds a safe migration plan (export format matrix, dedupe/merge precedence rules, TOTP and attachment traps, 2FA-site re-enrollment list), generates the field-mapping worksheet, and runs a post-migration audit for duplicates, weak leftovers, and reused entries. Never touches actual secrets — works from counts and metadata you paste.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [passwords, password-manager, migration, bitwarden, 1password, keepass, security]
---

# Password Manager Migrator

Migrating password managers is one of the highest-stakes household data
moves: do it wrong and you lose TOTP seeds, attachments, and folder
structure — or silently drop accounts you won't notice for a year. The
export formats don't map 1:1 (Bitwarden JSON has folders + TOTP; KeePass
has groups + icons + history; Chrome CSV loses both), and every path has
specific traps.

This skill builds the migration plan, never touching your secrets: it
works from metadata (counts, formats) and produces checklists, worksheets,
and the audit logic.

## When to Use

- Switching managers (any direction among Bitwarden, 1Password, KeePass,
  Chrome/Safari, Proton Pass)
- Merging two vaults (personal + inherited, couple merge, work split)
- Post-migration audit: what didn't survive the import
- Deciding WHICH route: direct import vs CSV vs JSON

**Don't use for:** live secret values — nothing here ever needs your
actual passwords. If a tool asks for them outside the manager itself, stop.

## The Method

1. **`plan`** — from → to: the best route (native import > JSON > CSV),
   what transfers and what's LOST per hop, ordered steps with checkpoints,
   rollback point (keep the old vault read-only for 30 days).
2. **`worksheet`** — the field-mapping CSV template + precedence rules for
   duplicates (newer modified-date wins; conflicts flagged for manual
   review, never auto-merged silently).
3. **`totp`** — TOTP inventory + re-enrollment list: which sites' 2FA won't
   survive and must be re-enrolled BEFORE deleting anything.
4. **`audit`** — paste counts (pre/post item counts per type, duplicates
   found, weak flags) → verification verdict + residual-risk list.

## Quick Start

```bash
# Bitwarden -> 1Password
python3 scripts/vault_migrate.py plan --from bitwarden --to 1password

# Merge two Bitwarden vaults (couple merge)
python3 scripts/vault_migrate.py plan --from bitwarden --to bitwarden --merge

# The TOTP trap list for Chrome CSV hop
python3 scripts/vault_migrate.py totp --via csv

# Post-migration numbers check
python3 scripts/vault_migrate.py audit --pre-logins 412 --post-logins 398 \
    --pre-notes 55 --post-notes 55 --pre-cards 9 --post-cards 9 \
    --duplicates 41 --weak-left 23

# Field mapping worksheet (CSV) for the hop
python3 scripts/vault_migrate.py worksheet --from keepass --to bitwarden
```

Stdlib-only Python 3. Offline. Zero network. Zero secrets.

## Route Matrix (what the script encodes)

| From → To | Best route | Survives | LOST |
|---|---|---|---|
| Bitwarden → 1Password | 1P native Bitwarden importer | logins, notes, cards, TOTP | folders→tags (approx), attachments (manual) |
| 1Password → Bitwarden | BW native 1P importer (or 1PIUX→enc JSON) | logins, notes, TOTP | tags, attachments, document count check |
| KeePass → Bitwarden | BW native KP importer | logins, notes, TOTP (otp field), groups→folders | icons, entry history, auto-type |
| Any → Chrome | CSV only | URL/user/pass | TOTP, folders, notes attachments, card CVV |
| Chrome → Bitwarden | BW native Chrome importer | logins | passwords saved after last export |
| Proton ↔ Bitwarden | Proton importer / BW importer | logins, notes | Proton aliases need email-forward check |

## The Traps (ranked by pain)

1. **TOTP seeds are one-shot.** Exported seeds that fail to import are
   RECOVERABLE ONLY by re-enrolling each site (needs password + working
   2FA). Inventory BEFORE deleting the old vault.
2. **Chrome CSV drops TOTP + everything but URL/user/pass** — fine as an
   intermediate, fatal as "the migration."
3. **Attachments don't ride exports.** Count them; they move manually or
   get re-added as secure notes/attachments.
3. **Modified-date lies after CSV hops** (export date replaces it) — breaks
   "newer wins" dedupe. Prefer JSON/native routes when merging.
4. **Duplicate storm after merge.** Import everything, dedupe INSIDE the
   target, never pre-dedupe two half-copies.
5. **Old vault deleted too early.** Keep read-only 30 days; the login you
   need in week 3 WILL be the one that didn't import.

## Common Pitfalls

1. **Doing the export on a machine you're about to wipe.** Export + import
   + audit on stable hardware, then wipe.
2. **Unencrypted JSON export left in Downloads.** The export contains
   EVERYTHING in plaintext. Secure-delete it after verified import; never
   let it touch cloud sync folders.
3. **Trusting the importer's success message.** Count-based audit (pre vs
   post per type) is the only real verification.
4. **Merging and migrating in one step.** Two operations, two audits.
5. **Ignoring password-based (not link-based) sharing entries** — shared
   items need re-sharing from the new vault, they don't migrate.

## Verification Checklist

- [ ] Export created (count items per type first — that's your pre-count)
- [ ] Import done into the TARGET with 2FA on the account already
- [ ] `audit` run with pre/post counts — deltas explained
- [ ] TOTP re-enrollment list worked through (each site: old code still
      valid → enroll new → verify → note it)
- [ ] Attachments count matches
- [ ] Plaintext export secure-deleted
- [ ] Old vault kept read-only 30 days, calendar reminder set
- [ ] One real login test per category (bank, email, shopping)

## References

- `references/route-matrix.md` — full per-hop details, per-manager export
  menu paths, importer quirks, encrypted-export options
- `references/audit-worksheet.md` — the dedupe precedence rules, TOTP
  re-enrollment protocol, merge conflict workflow, 30-day cutover plan
