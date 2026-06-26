# Session Monitor — Reference

## Architecture
```
index.js      — main loop: poll JSONL files, accumulate, send/edit Telegram messages
parser.js     — parse JSONL entries into {sender, text} display objects
formatter.js  — merge same-sender messages, sort sessions, build HTML
sender.js     — Telegram API: sendMessage / editMessageText with queue
sessions.js   — session key lookup, tag formatting, subagent name resolution
```

## Configuration (index.js)
```js
POLL = 3000         // poll interval (ms)
MERGE_WINDOW = 1    // merge edits within N minutes into one Telegram message
```

## Session Tags (sessions.js)

### User-configurable maps
```js
CHANNEL_ICONS = { telegram: '✈' }              // channel → icon
DIRECT_NAMES  = { 'direct:123456789': 'Agent↔Alice' }  // direct chat → display name
GROUP_NAMES   = { 'group:-100123456789': 'My Group' } // group → display name
```

### Display format
| Type | Format | Example |
|------|--------|---------|
| External direct | `{icon} {name}` | `✈ Agent↔Alice` |
| External group | `{icon} {name}` | `✈ My Group` |
| Subagent | `👶∙{name}∙{uuid}` | `👶∙fizz-buzz∙f93846d6` |
| Main CLI | `main` | `main` |
| Heartbeat | `main∙💓` | `main∙💓` |

### Subagent name resolution
1. `sessions.json` label field (set by `sessions_spawn` label arg)
2. JSONL content: matches `/prompts/{HOLE}.txt` in task text
3. Fallback: short UUID

### Sort order (top → bottom)
1. Internal (main, heartbeat)
2. 👶 subagents
3. External groups
4. External direct (always last)

## Message Format (parser.js)

### Senders
| Icon | Role |
|------|------|
| 🤖 | Assistant (text + tool calls) |
| 👤 | Real user input |
| ⚡ | System-injected (heartbeat, subagent context) |
| ↩️ | Tool result |
| ⚙️ | System prompt |

### Tool Calls (🤖 → tool)
Format: `<b>name</b> <b>target</b> <i>args</i>`

| Tool | Target | Args | Example |
|------|--------|------|---------|
| exec | program name | rest of command (50 chars) | **exec** **python3** *-c "print(1)"...* |
| read | filename | — | **read** **GOLF_TIPS.md** |
| write | filename | — | **write** **parser.js** |
| edit | filename | — | **edit** **sessions.js** |
| spawn | — | task (40 chars) | **spawn** *Read the file /tmp/...* |
| search | — | query (40 chars) | **search** *rust code golf tips* |
| fetch | URL (40 chars) | — | **fetch** **https://example.com** |
| poll | — | action:sessionId | **poll** *poll:warm-lake* |

### Tool Results (tool → 🤖)
Format: `↩️ │ 「content」`

| Result | Meaning |
|--------|---------|
| 「✅」 | Success, no output |
| 「✗ exit=1」 | Failed |
| 「⏳」 | Still running |
| 「exit=0」 | Process exited (poll) |
| 「✅ parser.js」 | Write/edit success |
| 「run」 | Spawn mode |
| 「content text...」 | Output (80 chars) |

### Special messages
| Display | Meaning |
|---------|---------|
| 🤖 │ 〔〕 | NO_REPLY |
| 🤖 │ 💤 | ANNOUNCE_SKIP |
| 🤖 │ text 💤 | HEARTBEAT_OK |
| 🤖 │ … | Empty message |

### Truncation
- General text: 300 chars + `...`
- Exec args: 50 chars + `...`
- Filenames > 30 chars: first 4 + `...` + last 23 (e.g. `samp...long-filename-test.md`)
- Tool results: 80 chars + `...` (read: 60 if > 100)

### Separator
All lines use `│` (pipe) between sender icon and content: `🤖 │ text`

## User message parsing
- Messages with `Conversation info (untrusted` → `👤` (real user input), metadata stripped
- Messages with `Read HEARTBEAT.md` → `⚡ 💓 heartbeat ping`
- Messages > 1000 chars → `⚡` with 80-char preview
- Other short messages → `⚡` with metadata stripped

### Metadata stripping (stripMeta)
Removes: `Conversation info (untrusted...````, `Sender (untrusted...````, `Replied message (untrusted...````, fenced JSON blocks, `[Queued messages...]`, `System: [...]` lines.

## Telegram delivery (sender.js + index.js)
- Poll every 3s for new JSONL entries
- Same time-window (MERGE_WINDOW minutes): `editMessageText` to update existing message
- New window: `sendMessage` to create new message
- Message > 4000 chars: truncate + force new message next poll
- Rate limit: 3s gap between API calls
