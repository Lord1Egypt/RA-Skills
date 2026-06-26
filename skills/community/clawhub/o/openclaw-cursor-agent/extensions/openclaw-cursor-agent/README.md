# openclaw-cursor-agent

OpenClaw plugin for managing persistent Cursor CLI coding tasks through tmux sessions.

## Architecture

```text
OpenClaw → plugin → WSL → tmux → Cursor CLI Agent
```

## Tools

| Tool | Description |
|------|-------------|
| `cursor_agent_spawn_task` | Start a background Cursor coding task |
| `cursor_agent_list_tasks` | List all recorded tasks |
| `cursor_agent_check_status` | Check task status, progress, and output |
| `cursor_agent_send_command` | Send follow-up instructions to a running task |
| `cursor_agent_kill_session` | Stop a running task |
| `cursor_agent_doctor` | Diagnose environment and dependencies |

## Chat Commands

```
/cursor doctor              — Check environment
/cursor list                — List tasks
/cursor status <session>    — Check task status
/cursor send <session> <msg> — Send instruction
/cursor kill <session>       — Stop task
/cursor spawn <name> || <description> || [path]
```

## Configuration

In `openclaw.json`:

```json
{
  "openclaw-cursor-agent": {
    "enabled": true,
    "config": {
      "toolkitRoot": "C:/Users/YOU/.openclaw/workspace/cursor-agent-system",
      "defaultProjectPath": "D:/project/your-project",
      "executionMode": "wsl",
      "timeoutMs": 120000,
      "shell": {
        "executable": "C:/Windows/System32/wsl.exe",
        "args": [],
        "wslDistro": "Debian"
      }
    }
  }
}
```

## WSL Dependencies

Inside WSL, ensure these are installed:

- `bash`, `tmux`, `python3` (via `apt`)
- Cursor CLI (`agent`) with valid login
- Node.js (if Cursor CLI bundled binary is incompatible)
