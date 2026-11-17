# Route Matrix — Full Reference

## Export locations (as of late 2026 — UIs drift, verify)

| Manager | Export path | Formats |
|---|---|---|
| Bitwarden | Web vault → Tools → Export vault | JSON (unencrypted), JSON (encrypted), CSV |
| 1Password | 8: File → Export → {vault} | .1pux (all data), CSV |
| KeePass (XC) | Database → Export | XML (KDBX 2.x), CSV, HTML |
| Chrome | chrome://passwords/settings → Export | CSV |
| Safari | Settings → Passwords → ⋯ → Export | CSV (Mac only) |
| Proton Pass | Settings → Import & export | JSON, CSV |

## Hop details

### Bitwarden → 1Password
Native importer handles logins/notes/cards/TOTP. Folder structure becomes
tags, loosely. Attachments (premium feature) must be downloaded and
re-attached manually — COUNT them first. Shared collection items need
re-sharing from inside 1Password.

### 1Password → Bitwarden
Export .1pux → Bitwarden's importer. Multi-vault setups collapse — do one
1Password vault per import and file into Bitwarden folders per vault.
Documents/attachments ride the .1pux but Bitwarden attachment handling
differs (count-check). Watchtower items are computed, not exported.

### KeePass → Bitwarden
Export KeePass 2.x XML (not CSV — loses TOTP + groups). Groups map to
folders one level deep; nested groups flatten with separators. Entry
history and icons are lost (icons are cosmetic; history matters if you
used it as an audit trail — archive the .kdbx instead of deleting).

### Chrome → anywhere
Export CSV has exactly: name, url, username, password. Everything else in
Chrome's store (TOTP, passkeys, addresses) does not export. Also: anything
saved after the export moment is missing — re-export right before final
cutover if Chrome was still in use.

### Proton ↔ Bitwarden
JSON both ways. The real trap is hide-my-email aliases: they live as email
addresses in logins, but the forwarding is a Proton service — verify at
least one alias still routes after migration before deleting the Proton
account.

### Safari
iCloud Keychain TOTP codes don't export at all; secure notes export only
on Mac. Passkeys stay in Apple's ecosystem (for now) — inventory them
separately if you rely on them.

## Encrypted export options

- Bitwarden: password-encrypted JSON export (safe to store/transfer) —
  but ONLY Bitwarden can re-import it. Use for backup, not migration.
- 1Password: .1pux is unencrypted when exported — same handling rules.
- Rule: unencrypted exports exist only on the working machine, in a
  non-synced directory, for minutes; `srm`/secure-delete after.

## Importer quirks worth knowing

- Importers run per-user, not per-org: import to your account, then move
  items into organizations/collections.
- Rate limits: very large imports (5k+ items) can time out — split into
  2-3 imports.
- Name-less entries and non-ASCII names are the classic silent drops;
  if your count audit fails, look there first.
- Duplicate detection: most targets only flag EXACT URI+username matches.
  www/non-www and http/https variants need your normalization.

## 30-day cutover plan

Day 0: export, import, audit, spot-check, secure-delete export.
Day 0: old vault → read-only (remove extension auto-fill, keep data).
Day 1–7: daily use on the new manager; note anything missing.
Day 7: TOTP re-enrollment complete; recovery codes stored.
Day 30: final diff of counts; delete old vault; revoke old account if
it's a service (export its data first if anything remains).
