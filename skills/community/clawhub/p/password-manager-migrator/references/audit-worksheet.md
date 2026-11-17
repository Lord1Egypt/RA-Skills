# Audit Worksheet — Reference

## Why count-based audit works

Importers report success while dropping items. The only trustworthy
verification is arithmetic: count per item type before export, count after
import, explain every delta. Five minutes of counting beats an hour of
trust.

| Type | Pre | Post | Delta | Explanation |
|---|---|---|---|---|
| Logins | | | | |
| Secure notes | | | | |
| Cards | | | | |
| Identities | | | | |
| TOTP entries | | | | |
| Attachments | | | | |

Deltas you may legitimately see:
- Post < pre after a merge with dedupe: delta = duplicates removed (check
  the tool's report count).
- Post > pre: you imported into a vault that already had items.
Deltas you may NOT see: unexplained losses. Those are silent drops —
find them before cutover.

## Finding silent drops

1. Export BOTH sides (source export you already have; re-export the
   target).
2. Normalize: sort by lowercase URI + username.
3. Diff — command-line (`jq`, `diff` on normalized CSVs) or a spreadsheet
   VLOOKUP on the URI+username key.
4. Usual suspects: entries with blank names, unicode-heavy names, notes
   >10 KB, attachments (always), items in folders the importer maps
   nowhere.

## Dedupe precedence rules

1. Exact URI + username → keep the NEWER modified-date entry.
2. Same username, URI variants (http/https, www, trailing /) → normalize
   the URI, then rule 1.
3. Same site, different usernames → KEEP BOTH (role/personal accounts).
4. Entry with password vs entry without → keep with password.
5. Undecidable in 5 seconds → "review" flag, manual look. Never let the
   tool auto-resolve conflicts you wouldn't bet an account on.

After CSV hops, modified-dates are meaningless (export date) — dedupe on
content: password differs → newer password is usually a rotation, but
verify on the site's "last changed" if it matters.

## TOTP re-enrollment protocol

For every entry that had TOTP in the source but not in the target:

1. Log in to the site (password + backup code or old TOTP still valid).
2. Security/2FA settings → enroll authenticator app → scan QR into the
   NEW manager.
3. Verify the new code works (the site asks to confirm a code).
4. Save new recovery codes as a secure note.
5. Mark the entry done.

Order matters: email first (it's the recovery path for everything else),
then financial, then the rest.

## Merge workflow (two vaults, one manager)

1. Import secondary export into a dedicated folder ("merge-inbox").
2. Run the target's duplicate report across the whole vault.
3. Apply precedence rules; conflicts to a review list.
4. Empty the inbox folder as items resolve; anything unresolved after a
  week gets a decision (usually: both accounts are real).
5. Count check: pre1 + pre2 − removed-dupes = post.

## Post-migration hygiene (the audit's tail)

- Weak/reused leftovers: the target's security report lists them; rotate
  email → bank → shopping → everything else.
- Recovery codes stored as secure notes (they didn't migrate as such).
- Emergency access / inheritance: set it up in the new manager (Kit/panic
  documents reference the vault, not the passwords).
- Old manager's browser extension: remove after cutover to avoid two
  auto-fill engines fighting.
