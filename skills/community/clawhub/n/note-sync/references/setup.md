# Setup Guide

## Architecture

```
ClawHub Skill (~/.openclaw/skills/note-sync/)
  └── scripts/note-sync-mcp.sh  ──exec──►  $NOTE_SYNC_REPO/mcp-server/note-sync-mcp.exe
                                                      └── notes/*.md
```

ClawHub ships the **skill** (instructions + launcher script). The **MCP binary** comes from the [go-note-sync-mcp](https://github.com/your-org/go-note-sync-mcp) repo and must be built on Windows.

## Path convention

| Item | Path |
|------|------|
| Repo root | `$NOTE_SYNC_REPO` (env var) |
| MCP exe | `$NOTE_SYNC_REPO/mcp-server/note-sync-mcp.exe` |
| Notes | `$NOTE_SYNC_REPO/mcp-server/notes/` |
| Skill launcher | `~/.openclaw/skills/note-sync/scripts/note-sync-mcp.sh` |

## Install from ClawHub

```bash
openclaw skills install note-sync --global
chmod +x ~/.openclaw/skills/note-sync/scripts/note-sync-mcp.sh
```

## Build MCP (Windows PowerShell)

```powershell
git clone https://github.com/your-org/go-note-sync-mcp.git
cd go-note-sync-mcp\mcp-server
go build -o note-sync-mcp.exe
```

## Configure OpenClaw (WSL)

Edit `~/.openclaw/openclaw.json` — see [`openclaw.json.example`](openclaw.json.example).

Required fields:

1. `skills.entries.note-sync.env.NOTE_SYNC_REPO` — WSL path to repo root
2. `mcp.servers.note-sync.command` — skill launcher or direct exe path

### Option A — Launcher script (recommended)

MCP command uses the skill-bundled script; script reads `NOTE_SYNC_REPO` and runs `mcp-server/note-sync-mcp.exe`:

```json
{
  "skills": {
    "entries": {
      "note-sync": {
        "enabled": true,
        "env": {
          "NOTE_SYNC_REPO": "/mnt/e/github/go-note-sync-mcp"
        }
      }
    }
  },
  "mcp": {
    "servers": {
      "note-sync": {
        "command": "/home/lg/.openclaw/skills/note-sync/scripts/note-sync-mcp.sh",
        "args": []
      }
    }
  }
}
```

### Option B — Direct exe path

```json
{
  "mcp": {
    "servers": {
      "note-sync": {
        "command": "/mnt/e/github/go-note-sync-mcp/mcp-server/note-sync-mcp.exe",
        "args": []
      }
    }
  }
}
```

Option B still requires `NOTE_SYNC_REPO` in `skills.entries` for skill gating (Ready status).

## Verify

```bash
openclaw gateway restart
openclaw skills info note-sync
openclaw mcp show note-sync
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Needs setup △ | Set `NOTE_SYNC_REPO` and `mcp.servers.note-sync` |
| MCP binary not found | Run `go build` on Windows |
| Permission denied on script | `chmod +x ~/.openclaw/skills/note-sync/scripts/note-sync-mcp.sh` |
| Wrong notes location | Notes are always next to exe: `mcp-server/notes/` |

## WSL path mapping

| Windows | WSL |
|---------|-----|
| `E:\github\go-note-sync-mcp` | `/mnt/e/github/go-note-sync-mcp` |
| `D:\projects\go-note-sync-mcp` | `/mnt/d/projects/go-note-sync-mcp` |
