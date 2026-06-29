# Pi Keyboard Shortcuts

## Interactive Mode

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message (while agent running = steering) |
| `Alt+Enter` | Follow-up message (sent after agent completes) |
| `Ctrl+C` | Clear editor |
| `Ctrl+C` ×2 | Quit |
| `Escape` | Cancel/Abort |
| `Escape` ×2 | Open /tree |
| `Ctrl+L` | Model selector |
| `Ctrl+P` | Cycle to next model (scoped) |
| `Shift+Ctrl+P` | Cycle to previous model (scoped) |
| `Shift+Tab` | Cycle thinking level |
| `Ctrl+O` | Collapse/expand tool output |
| `Ctrl+T` | Collapse/expand thinking blocks |
| `Tab` | Path completion |
| `Shift+Enter` | Multi-line input (Windows Terminal: `Ctrl+Enter`) |
| `Esc` ×3 | Abandon + clear queue |
| `Alt+Up` | Restore queued message to editor |

## Editor Shortcuts

- `@` — fuzzy search project files
- `!command` — execute bash command and send output to LLM
- `!!command` — execute bash command (not sent to LLM)
- `Ctrl+V` — paste image (Windows: `Alt+V`)

## /tree Navigation

| Shortcut | Action |
|----------|--------|
| Type | Search |
| `Ctrl+←` / `Alt+←` | Previous branch |
| `Ctrl+→` / `Alt+→` | Next branch |
| `←` / `→` | Page up/down |
| `Ctrl+O` | Toggle filter mode: default → no-tools → user-only → labeled-only → all |
| `Shift+L` | Toggle bookmark |
| `Shift+T` | Toggle bookmark timestamp display |

## CLI Arguments

```bash
pi -p "query"                        # print mode
pi --mode json                       # JSON event stream
pi --mode rpc                        # RPC (stdin/stdout LF-delimited JSONL)
pi -c                                # continue most recent session
pi -r                                # browse session list
pi --session <path|id>               # use specified session
pi --fork <path|id>                  # fork session to new session
pi --new / --no-session              # new session / don't save
pi --no-context-files / -nc          # skip AGENTS.md loading
pi --offline                         # offline mode
```