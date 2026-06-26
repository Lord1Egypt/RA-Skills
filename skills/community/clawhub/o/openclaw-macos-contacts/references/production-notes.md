# Production notes

## Why split reads and writes

Using SQLite for reads gives speed and flexible search. Using AppleScript for writes avoids corrupting the Contacts DB and lets macOS handle supported object creation.

## Operational guidance

- Back up the DB before experiments that inspect schema or test nonstandard behavior.
- For user-facing automation, default to idempotent behavior where possible.
- For create operations, implement duplicate checks on name + phone/email before writing.
- For future extension, consider Swift + Contacts.framework if you need large-scale sync, update, delete, or merge workflows.
