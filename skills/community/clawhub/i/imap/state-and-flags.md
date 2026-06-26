# State, Flags, and Sync Rules

Use this file for anything involving durability, mailbox state, or incremental sync.

## Durable Identifiers

- `UID` is stable within a folder only while `UIDVALIDITY` stays the same.
- Sequence numbers are session-local positions and can drift immediately.
- If `UIDVALIDITY` changes, invalidate stored cursors and rebuild state.

## Useful Sync Markers

- `UIDNEXT` estimates where new mail may start.
- `HIGHESTMODSEQ` matters for `CONDSTORE` or `QRESYNC` capable servers.
- The last processed UID should be tracked per account and folder, not globally.

## Common Flags

| Flag | Meaning | Notes |
|------|---------|-------|
| `\\Seen` | message has been marked read | can change user-visible inbox state |
| `\\Answered` | message has been replied to | not all providers expose it consistently |
| `\\Flagged` | starred or important marker | semantics vary by provider |
| `\\Deleted` | marked for deletion | not always removed until expunge |
| `\\Draft` | draft state | usually irrelevant for read-only triage |

Custom keywords may exist. Do not assume only the standard system flags are present.

## Mutation Safety

- `STORE` changes flags and may affect client-visible state immediately.
- `MOVE` is safer than copy-plus-delete when the server supports it, but still changes mailbox state.
- `EXPUNGE` is destructive because it permanently removes messages already marked deleted.
- A dry run should identify affected UIDs before performing any bulk change.

## Folder Semantics

- Archive, All Mail, Sent, Junk, and Trash are provider-specific concepts.
- Some providers expose labels or virtual folders through IMAP in ways that do not behave like classic folders.
- Capture provider quirks in `folder-map.md` so future sessions do not rediscover them.

## Incremental Sync Pattern

1. Check `UIDVALIDITY`.
2. Resume from saved UID window or `MODSEQ`.
3. Fetch only changes since the last checkpoint.
4. Reconcile deletions, moves, and flag changes explicitly.
5. Update `sync-state.md` only after the pass is confirmed.
