# memory-lcm — Lossless Context Manager

**Tony Spark LCM** — Lossless conversation memory for OpenClaw agents.

Stores every message in SQLite, creates chunk + daily summaries, auto-syncs key decisions to MEMORY.md.

## Setup

```bash
cd skills/memory-lcm
npm install
```

## CLI Commands

```bash
node bin/tony-lcm.js status              # Show DB stats
node bin/tony-lcm.js search <query>     # Search full history
node bin/tony-lcm.js recall <topic> [d] # Recall topic (default 7 days)
node bin/tony-lcm.js compact [session]  # Compact messages → summaries
node bin/tony-lcm.js daily [session]   # Generate daily summary
node bin/tony-lcm.js sync [session]     # Sync decisions → MEMORY.md
```

## Code Usage

```javascript
const { MemoryLCM } = require('./skills/memory-lcm/src');

const lcm = new MemoryLCM('my-session');
await lcm.init();

// After each turn:
lcm.log('user', userMessage);
lcm.log('assistant', assistantResponse);

// End of day or when context is high:
lcm.compact();

// Recall:
const results = lcm.search('forest scene');
const history = lcm.recall('Sig Botti OS', 14);
```

## How It Works

```
Level 2: Daily Summaries (coarse)
Level 1: Chunk Summaries (20 msgs each)
Level 0: Raw Messages (recent, protected)
Storage: SQLite (sql.js) → ~/.openclaw/workspace/data/tony-lcm.db
Auto-sync: Key decisions → MEMORY.md
```

## Key Features

- ✅ Lossless — every message stored, nothing truncated
- ✅ Searchable — full-text search across all sessions
- ✅ Auto-sync — decisions auto-append to MEMORY.md
- ✅ No native deps — sql.js (WASM) works everywhere
- ✅ Session isolation — each session separate in DB
- ✅ Compaction — summaries older messages, keeps recent raw
