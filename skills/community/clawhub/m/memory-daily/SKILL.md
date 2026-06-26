---
name: memory-daily
description: Automates daily memory file management. Use when creating, reading, or appending to daily memory notes (memory/YYYY-MM-DD.md). Helps the agent maintain continuity across sessions without manual file editing.
---

# memory-daily

Manages daily memory files in `memory/YYYY-MM-DD.md`.

## Functions

### `ensureToday(memoryDir?)`
Creates today's daily file if it doesn't exist. Returns the file path.

### `append(entry, memoryDir?)`
Appends a timestamped entry to today's daily file. Creates the file first if needed.

### `read(date?, memoryDir?)`
Reads a daily file. Defaults to today. Date format: `YYYY-MM-DD`.

### `recent(days?, memoryDir?)`
Returns content from the last N days (default 2).

## Usage

```js
const mem = require('./skills/memory-daily');

// Ensure today's file exists
await mem.ensureToday();

// Append an entry
await mem.append('## Session Notes\n- Deployed new feature X');

// Read today
const today = await mem.read();

// Read last 3 days
const recent = await mem.recent(3);
```

## Default memory directory
`<workspace>/memory/`
