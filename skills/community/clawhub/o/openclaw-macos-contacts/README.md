# openclaw-macos-contacts

Production-grade macOS Contacts skill for OpenClaw.

## What it does

This skill provides a safe, production-oriented workflow for working with native macOS Contacts:

- Fast contact reads/search via SQLite
- Native contact create/update/delete via Swift + `Contacts.framework`
- Duplicate detection and duplicate-group planning
- Merge/dedupe flows with backup + rollback support
- Transaction wrapper for mutating operations

## Design

- **Read path:** SQLite (`AddressBook-v22.abcddb`) for speed and flexible search
- **Write path:** Swift + `Contacts.framework` for supported native mutations
- **Fallback path:** AppleScript / Contacts.app for compatibility scenarios
- **Safety:** backup, restore, transactional wrapper, explicit identifier-based delete/update

## Key scripts

- `scripts/contacts_sqlite.py`
- `scripts/contacts_swift.swift`
- `scripts/contacts_merge.swift`
- `scripts/contacts_backup.sh`
- `scripts/contacts_restore.sh`
- `scripts/contacts_txn.sh`
- `scripts/contacts_dedupe.sh`

## Examples

```bash
# Search contacts
python3 scripts/contacts_sqlite.py search "Alice"

# Native find
swift scripts/contacts_swift.swift find --query "Alice"

# Create contact with transaction backup
bash scripts/contacts_txn.sh swift scripts/contacts_swift.swift create \
  --first-name Alice \
  --last-name Example \
  --phone 15555550123 \
  --email alice@example.com

# Update contact by identifier
bash scripts/contacts_txn.sh swift scripts/contacts_swift.swift update \
  --identifier "CONTACT_ID" \
  --organization "Example Inc" \
  --job-title "Manager"

# Plan duplicate merges
swift scripts/contacts_merge.swift plan-duplicates
```

## Safety notes

- Do not write directly to the Contacts SQLite DB.
- Use native APIs for writes.
- Wrap destructive or mutating operations with `contacts_txn.sh`.
- Runtime backup state is intentionally stored outside the skill directory.

## Status

Current repo status: production-capable skill, suitable for private/internal use and further iteration.

## 中文说明

- 参见 `README.zh-CN.md`
