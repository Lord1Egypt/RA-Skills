---
name: session-monitor
description: "Real-time OpenClaw session monitor that tails JSONL transcripts and pushes formatted updates to Telegram as a persistent background process. Use when asked to monitor, watch, observe, track, spy on, or tail agent sessions, set up a live feed or dashboard of agent activity, deploy a background monitor with Telegram push notifications, or restart/stop/check the monitor. Triggers: monitor sessions, watch agent, start monitor, restart monitor, stop monitor, monitor status, session dashboard, live feed, tail sessions, what is the agent doing, observe agent, track activity, spy on agent, background monitor, push notifications, 监控session, 监控agent, 盯着agent, 看看agent在干嘛, 实时监控, 后台监控, 订阅session, agent活动推送, 重启监控, 停止监控, 监控状态. NOT for one-shot session inspection (use built-in sessions_list / sessions_history for that)."
---

# Session Monitor

Persistent background process that polls all JSONL transcript files in an
agent's session directory, parses new entries, and pushes formatted HTML
updates to a Telegram chat. Messages within the same time window are merged
via `editMessageText` to avoid spam.

## When to Use

- User wants **continuous, push-based** monitoring of agent activity
- User wants a **live dashboard** in a Telegram chat showing what the agent does
- NOT for one-shot queries — use `sessions_list` / `sessions_history` instead

## Quick Start

```bash
# 1. Configure
cp scripts/.env.example scripts/.env
# Edit scripts/.env with bot token, chat ID, session dir, user/group mappings

# 2. Dry-run (verify parsing works)
node scripts/test.js

# 3. Start (exec session safe — won't die when agent session ends)
node scripts/index.js > scripts/monitor.log 2>&1 &
```

⚠️ **Agent exec sessions:** Processes started via `nohup &` inside an
agent's `exec` tool may be killed when the exec session is cleaned up.
Add a watchdog to your HEARTBEAT.md to auto-restart:

```bash
PID=$(cat scripts/.pid 2>/dev/null)
if [ -z "$PID" ] || ! ps -p "$PID" > /dev/null 2>&1; then
  cd scripts && node index.js > monitor.log 2>&1 &
fi
```

## Configuration (.env)

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | ✅ | Telegram bot token for sending updates |
| `CHAT_ID` | ✅ | Target Telegram chat ID (group or DM) |
| `AGENTS` | ❌ | Multi-agent: `Name\|/path/to/sessions,Name2\|/path2` |
| `AGENT_NAME` | ❌ | Single-agent display name (fallback when `AGENTS` unset) |
| `SESSIONS_DIR` | ❌ | Single-agent session dir (default: `~/.openclaw/agents/main/sessions`) |
| `DIRECT_USERS` | ❌ | Direct chat mappings: `userId:Name,userId2:Name2` |
| `GROUPS` | ❌ | Group chat mappings: `groupId:Name,groupId2:Name2` |

Display format: direct chats show as `✈ AgentName↔UserName`, groups as `✈ GroupName`.

## Architecture

```
scripts/
├── index.js      — Main loop: poll JSONL, accumulate, send/edit Telegram messages
├── parser.js     — Parse JSONL entries into {sender, text} display objects
├── formatter.js  — Merge same-sender messages, sort sessions, build HTML
├── sender.js     — Telegram API: sendMessage / editMessageText with queue
├── sessions.js   — Session key lookup, tag formatting, subagent name resolution
├── config.js     — Load .env configuration
├── test.js       — Dry-run: parse recent entries and print to stdout
├── .env.example  — Configuration template
└── .env          — Local config (gitignored)
```

## Tuning

In `scripts/index.js`:
- `POLL = 3000` — Poll interval in ms (default 3s)
- `MERGE_WINDOW = 1` — Merge edits within N minutes into one Telegram message
- `NEW_MSG_THRESHOLD = 3000` — Start a new message when current exceeds this many chars

## Message Format

See `references/REFERENCE.md` for detailed format specification including:
- Sender icons (🤖 assistant, 👤 user, ⚡ system, ↩️ tool result)
- Tool call formatting and truncation rules
- Session tag formatting and sort order
- Telegram delivery and rate limiting

## Management

PID file at `scripts/.pid` is written on startup, cleaned on exit.
Always use the **full path** to avoid cross-monitor conflicts on shared machines:

```bash
# Check if running
SKILL_DIR=/path/to/session-monitor
cat "$SKILL_DIR/scripts/.pid" && ps -p $(cat "$SKILL_DIR/scripts/.pid") -o pid,command

# Stop
kill $(cat "$SKILL_DIR/scripts/.pid")

# View logs
tail -f "$SKILL_DIR/scripts/monitor.log"
```

⚠️ Multiple monitors may coexist on the same machine (each with its own
`.env`, `.pid`, and log). Always reference the correct skill directory.

## Restart / Stop / Status

Resolve `SKILL_DIR` to **this skill's directory** (parent of `scripts/`).

```bash
# Status — is monitor running?
SKILL_DIR=/absolute/path/to/session-monitor
PID=$(cat "$SKILL_DIR/scripts/.pid" 2>/dev/null)
if [ -n "$PID" ] && ps -p "$PID" > /dev/null 2>&1; then
  echo "✅ Monitor running (PID $PID)"
else
  echo "❌ Monitor not running"
fi

# Stop
kill $(cat "$SKILL_DIR/scripts/.pid")

# Start
cd "$SKILL_DIR/scripts" && node index.js > monitor.log 2>&1 &

# Restart (stop + start)
kill $(cat "$SKILL_DIR/scripts/.pid") 2>/dev/null; sleep 1
cd "$SKILL_DIR/scripts" && node index.js > monitor.log 2>&1 &
```

## Notes

- Zero dependencies — pure Node.js standard library
- Startup sends a sample banner message to verify connectivity
- Messages > 4000 chars are truncated and force a new message next poll
- Rate limit: 3s gap between Telegram API calls
