---
name: note-sync
description: Append notes to local Markdown files via MCP append_note. Use when the user asks to save ideas, reminders, or journal entries.
version: 1.0.2
homepage: https://github.com/your-org/go-note-sync-mcp
user-invocable: true
metadata: {"openclaw":{"emoji":"📝","primaryEnv":"NOTE_SYNC_REPO","requires":{"env":["NOTE_SYNC_REPO"],"config":["mcp.servers.note-sync"]},"envVars":[{"name":"NOTE_SYNC_REPO","required":true,"description":"Repo root path (WSL). MCP exe must exist at $NOTE_SYNC_REPO/mcp-server/note-sync-mcp.exe"}],"install":[{"id":"clone","kind":"manual","label":"Clone go-note-sync-mcp and set NOTE_SYNC_REPO to repo root"},{"id":"build","kind":"manual","label":"Windows: cd %NOTE_SYNC_REPO%\\mcp-server && go build -o note-sync-mcp.exe"},{"id":"mcp","kind":"manual","label":"Set mcp.servers.note-sync.command to {baseDir}/scripts/note-sync-mcp.sh"}]}}
---

# Note Sync

Save conversation content to local Markdown files using the MCP tool `append_note`.

## When to use

Invoke when the user wants to:

- Save an idea, insight, or reminder as a note
- Append content to a named note file (e.g. 感悟, 待办, journal)
- Persist text from the chat to disk

## One-time setup

ClawHub installs this skill to `~/.openclaw/skills/note-sync/`. Complete these steps once.

### Step 1 — Clone repo and build MCP (Windows)

```powershell
git clone https://github.com/your-org/go-note-sync-mcp.git
cd go-note-sync-mcp\mcp-server
go build -o note-sync-mcp.exe
```

MCP binary path (fixed convention):

```
$NOTE_SYNC_REPO/mcp-server/note-sync-mcp.exe
```

WSL example: `/mnt/e/github/go-note-sync-mcp/mcp-server/note-sync-mcp.exe`

### Step 2 — Configure `~/.openclaw/openclaw.json`

Replace `<WSL_REPO>` with your repo root in WSL (e.g. `/mnt/e/github/go-note-sync-mcp`).

Replace `<SKILL_DIR>` with your skill install path (default `~/.openclaw/skills/note-sync`).

```json
{
  "skills": {
    "entries": {
      "note-sync": {
        "enabled": true,
        "env": {
          "NOTE_SYNC_REPO": "<WSL_REPO>"
        }
      }
    }
  },
  "mcp": {
    "servers": {
      "note-sync": {
        "command": "<SKILL_DIR>/scripts/note-sync-mcp.sh",
        "args": []
      }
    }
  }
}
```

The bundled launcher `{baseDir}/scripts/note-sync-mcp.sh` runs `<WSL_REPO>/mcp-server/note-sync-mcp.exe`.

**Alternative:** point `mcp.servers.note-sync.command` directly to `<WSL_REPO>/mcp-server/note-sync-mcp.exe`.

### Step 3 — Restart and verify

```bash
openclaw gateway restart
openclaw skills info note-sync
openclaw mcp list
```

Status should be **Ready** and tool `append_note` should appear.

Copy-paste template: `{baseDir}/references/openclaw.json.example`

## Tool: append_note

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `title` | string | yes | Note title; used as filename |
| `content` | string | yes | Note body (Markdown supported) |

**Success:** `已保存笔记：{title}`

**Example call:**

```json
{
  "title": "感悟",
  "content": "手上有钱，身体健康，才是人生的巅峰。"
}
```

## Agent rules

1. Infer `title` from user intent (or use a short category like 感悟 / 待办).
2. Call `append_note` with `title` and `content`.
3. Confirm success and mention notes are stored under `<repo>/mcp-server/notes/`.

## References

- Full setup: `{baseDir}/references/setup.md`
- Tool spec: `{baseDir}/references/tool-reference.md`
- Config template: `{baseDir}/references/openclaw.json.example`
