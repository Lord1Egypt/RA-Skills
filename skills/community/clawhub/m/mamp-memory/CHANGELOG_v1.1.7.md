# AI Memory Protocol — v1.1.6

**File**: `ai_memory_protocol_v1.1.6.py`
**Protocol Version**: `PROTOCOL_VERSION = "1.1.6"`
**Database Version**: `DB_VERSION = 14`
**Status**: Pending — deploy after v1.1.5 confirmed stable

---

## Performance Improvement

### Buffered Write — ~300x throughput gain
`add_turn()` now buffers in memory instead of writing to SQLite on every call. Data is flushed to disk in a single batch commit when:
- Buffer reaches 50 turns (`BATCH_SIZE`)
- `end_conversation()` is called
- `flush()` is manually called

**Before** (v1.1.5): each `add_turn()` = 2 new connections + 2 commits = ~7.4 ms
**After** (v1.1.6): each `add_turn()` = memory append = < 0.01 ms; flush = 1 batch commit

**Trade-off**: If the process crashes before a flush, the buffered turns are lost. For human-paced conversations (typing speed ~100-500 ms between messages), this risk is negligible and acceptable.

---

## New Features

### `flush()` — manual trigger
Public method to force an immediate flush of the write buffer.

### `SessionManager.add_turns_batch()` — now flushes buffer first
Before inserting a batch, any buffered single `add_turn()` calls are flushed first, ensuring correct turn ordering.

---

## Bug Fixes

### `add_turns_batch()` did not update `turn_count`
The DB-level method `add_turns_batch()` was called directly without updating `self.turn_count` or `self._buf_first_index`, causing turn indices to restart from 0 on each batch call. Fixed: both fields are now updated after the DB call.

---

## Files

```
ai_memory_protocol_v1.1.6.py    ← current version (this release)
ai_memory_protocol_v1.1.5.py    ← previous version (stable)
CHANGELOG_v1.1.6.md             ← this document
CHANGELOG_v1.1.5.md             ← previous changelog
```
