---
name: macos-contacts
description: Read, search, and safely create contacts in macOS Contacts (Address Book). Use when the user asks to inspect the native macOS contacts database, search contacts by name/phone/email/company, verify whether a contact exists, or add a new contact to Apple Contacts. Prefer this skill for production-grade contact access on macOS. Use SQLite for read-heavy search/list operations and AppleScript for writes, so reads stay fast and writes stay on supported system APIs.
---

# macOS Contacts

Use this skill for production-safe access to the local macOS Contacts data.

## Principles

- Prefer **SQLite** for reads/search/list because it is fast and flexible.
- Prefer **Swift + Contacts.framework** for production writes/checks because it uses the native contacts API directly and avoids AppleScript performance/pathology issues. Keep AppleScript as a compatibility fallback only.
- Do **not** write directly to the AddressBook SQLite database.
- Before any destructive or risky experiment, create a backup of the AddressBook database.
- For normal add-contact operations, writes are non-destructive and do not require touching the DB directly.

## Data locations

Primary Contacts database on macOS:

- `~/Library/Application Support/AddressBook/AddressBook-v22.abcddb`
- Sidecars may exist:
  - `AddressBook-v22.abcddb-wal`
  - `AddressBook-v22.abcddb-shm`

## Bundled scripts

### `scripts/contacts_sqlite.py`

Use for read/search/list against the native Contacts SQLite database.

Examples:

```bash
python3 scripts/contacts_sqlite.py list --limit 20
python3 scripts/contacts_sqlite.py search "黄"
python3 scripts/contacts_sqlite.py search "1555555"
python3 scripts/contacts_sqlite.py get --name "Huang Liao"
python3 scripts/contacts_sqlite.py exists --phone 15555550123
```

Output defaults to JSON for easy downstream use.

### `scripts/contacts_swift.swift`

Use for production-grade native contact API access via `Contacts.framework`.

Examples:

```bash
swift scripts/contacts_swift.swift count
swift scripts/contacts_swift.swift find --query "Huang"
swift scripts/contacts_swift.swift create   --first-name OpenClaw   --last-name Native   --phone 15555550124   --email native@example.com
```

Use this path for create and duplicate checks before write.

### `scripts/contacts_applescript.py`

Use for supported writes and API-level reads via Contacts.app.

Examples:

```bash
python3 scripts/contacts_applescript.py count
python3 scripts/contacts_applescript.py create \
  --first-name OpenClaw \
  --last-name Demo \
  --phone 15555550123 \
  --email demo@example.com
```

## Recommended workflow

### Read/search flow

1. Use `contacts_sqlite.py` for fast read/search.
2. If results are ambiguous, refine by phone/email/company.
3. Return structured results first; summarize after.

### Create-contact flow

1. Confirm target fields from the user when creating a real contact:
   - first name / last name or display name
   - phone and/or email
   - organization/job title if relevant
2. Use `contacts_swift.swift create` or `contacts_swift.swift update`.
3. Duplicate-check before create uses strict matching: phone exact match, email exact match, or full-name exact match when no phone/email is supplied; if a match exists, return it instead of creating a duplicate.
4. For updates, prefer identifier-based precise modification instead of fuzzy matching.
5. Read back the contact to verify success.
6. For delete, require identifier-based targeting and recommend wrapping the command with `contacts_txn.sh`.
7. Report exactly what changed.

## Safety rules

- Do not directly mutate the SQLite DB.
- Do not delete or merge contacts unless the user explicitly asks.
- Before delete/merge/batch update, create a backup or use `contacts_txn.sh`.
- Treat bulk writes as sensitive; prefer one verified create at a time unless the user explicitly wants batch import.
- If AppleScript permissions fail, report that Contacts automation permission is required.

## References

- Read `references/schema-notes.md` when you need table/field hints for SQLite queries.
- Read `references/production-notes.md` when designing higher-level automation on top of this skill.


## Backup and rollback

Use the bundled transaction helpers before destructive or multi-record write operations.

### `scripts/contacts_backup.sh`

Create a filesystem-level backup of the AddressBook DB and sidecars.

### `scripts/contacts_restore.sh`

Restore a backup directory back into the local AddressBook store.

### `scripts/contacts_txn.sh`

Wrap a mutating command with automatic pre-backup and rollback-on-failure.

Examples:

```bash
bash scripts/contacts_backup.sh
bash scripts/contacts_txn.sh swift scripts/contacts_swift.swift update --identifier "CONTACT_ID" --job-title "Manager"
bash scripts/contacts_restore.sh ~/.openclaw/state/macos-contacts/backups/AddressBook-YYYYmmdd-HHMMSS
```


## Dedupe cleanup

Use `scripts/contacts_dedupe.sh` only after listing duplicates and explicitly deciding which identifier to keep.

Example:

```bash
swift scripts/contacts_swift.swift duplicates
bash scripts/contacts_dedupe.sh KEEP_IDENTIFIER DROP_IDENTIFIER_1 DROP_IDENTIFIER_2
```

This workflow uses transactional delete wrappers so each delete is backed up and can roll back on failure.


## Dedupe merge

Use `scripts/contacts_merge.swift` to plan or apply a merge of duplicate contacts.

Examples:

```bash
swift scripts/contacts_merge.swift plan-duplicates
swift scripts/contacts_merge.swift apply-plan --keep KEEP_ID --drop DROP_ID_1 --drop DROP_ID_2
```

Recommended workflow:
1. Run `plan-duplicates`
2. Inspect the proposed keep/drop split
3. Wrap `apply-plan` with `contacts_txn.sh` before applying
