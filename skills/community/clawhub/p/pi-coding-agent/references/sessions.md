# Pi Session Management

Sessions are auto-saved to `~/.pi/agent/sessions/`, organized by working directory.

## CLI Arguments

```bash
pi -c                              # continue most recent session
pi -r                              # browse session history
pi --no-session                    # temporary mode (no save)
pi --session <path|id>             # specify a session
pi --fork <path|id>                # fork session to a new file
pi -r --offline                    # offline browsing
```

## Interactive Commands

| Command | Description |
|---------|-------------|
| `/resume` | Browse and select a past session |
| `/new` | New session |
| `/name <name>` | Set session display name |
| `/session` | Session details (file, ID, messages, tokens, cost) |
| `/tree` | Session tree navigation |
| `/fork` | Create new session from a past message |
| `/clone` | Copy current branch to a new session |
| `/export [file]` | Export to HTML |
| `/share` | Upload to GitHub Gist for sharing |
| `/compact [prompt]` | Manual compaction |

## Session Resume Interface

`/resume` and `pi -r` open an interactive picker:
- Type to search
- `Ctrl+P` toggle path display
- `Ctrl+S` toggle sort
- `Ctrl+N` show only named sessions
- `Ctrl+R` rename
- `Ctrl+D` delete (prefers trash CLI)

## Tree Navigation

Sessions are stored as a JSONL tree structure. Each entry has an id and parentId, with in-place branching (no new files).

```
├─ user: "Hello"
│ └─ assistant: "Hi!"
│   ├─ user: "Approach A" ← select to branch from here
│   │ └─ assistant: "..."
│   └─ user: "Approach B" ← select to branch from here
│     └─ assistant: "..."
```

| Command/Shortcut | Action |
|------------------|--------|
| `↑/↓` | Navigate visible entries |
| `←/→` | Page up/down |
| `Ctrl+←/→` or `Alt+←/→` | Expand/collapse or jump branch segments |
| `Shift+L` | Toggle bookmark |
| `Shift+T` | Toggle bookmark timestamp |
| `Enter` | Select |
| `Escape/Ctrl+C` | Cancel |
| `Ctrl+O` | Cycle filter mode |

Filter modes: default → no-tools → user-only → labeled-only → all. Set `treeFilterMode` config for default.

### Selection Behavior

- Select user/custom message → leaf moves to its parent, message placed in editor, editable for resubmission
- Select assistant/tool/compaction message → leaf moves to that entry, editor empty, continue from there
- Select root message → leaf reset to empty conversation, original prompt placed in editor

## /tree vs /fork vs /clone

| Feature | /tree | /fork | /clone |
|---------|-------|-------|--------|
| Output | Same session file | New file | New file |
| View | Full tree | User message picker | Current branch |
| Purpose | Explore alternatives in-place | Start fresh from past message | Backup before continuing |
| Summary | Optional branch summary | None | None |

## Branch Summary

When switching branches, Pi can auto-summarize the abandoned branch content and attach it to the new position. Options: no summary / default summary / custom focused summary.

## Compaction

- Manual: `/compact` or `/compact <instruction>`
- Auto: enabled by default, retries on context-full recovery / proactively compacts near limit
- Customizable: topic-based compaction or different model summaries via Extensions
- JSONL file retains full history (`/tree` can always go back)