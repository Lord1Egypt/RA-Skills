---
name: openclaw-session-viewer
description: Generate interactive HTML viewer for OpenClaw conversation sessions. Use when: (1) reviewing conversation history, (2) analyzing context management, (3) debugging session logs, (4) visualizing tool calls and results, (5) understanding token usage. Triggers on "view session", "conversation viewer", "session history", "context viewer", "review this conversation".
---

# OpenClaw Session Viewer

Generate an interactive HTML viewer for OpenClaw session logs with full conversation history, tool calls, and results.

## Quick Start

```bash
# Extract and view current session
python3 ~/.openclaw/skills/session-viewer/scripts/extract_session.py
open /tmp/session_viewer.html
```

## Commands

### Extract current session
```bash
python3 ~/.openclaw/skills/session-viewer/scripts/extract_session.py [--agent main] [--output /tmp/session_viewer.html]
```

### Extract specific session by ID
```bash
python3 ~/.openclaw/skills/session-viewer/scripts/extract_session.py --session-id <uuid>
```

### List available sessions
```bash
python3 ~/.openclaw/skills/session-viewer/scripts/extract_session.py --list
```

## Output

The viewer includes:
- **Sidebar**: All conversation turns with search
- **User messages**: Full raw text
- **Assistant responses**: Text + collapsible thinking blocks
- **Tool calls**: Full arguments JSON
- **Tool results**: Full output with status/exit code
- **Stats**: Token usage, cost, models used

## Session Log Location

```
~/.openclaw/agents/<agentId>/sessions/
├── sessions.json          # Index: session keys → IDs
└── <session-id>.jsonl     # Conversation log
```

## Tips

- Use keyboard navigation: ↑/↓ or j/k to browse turns
- Search filters across all fields (messages, tools, results)
- Click thinking header to expand/collapse
