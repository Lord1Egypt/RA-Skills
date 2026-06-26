---
name: openclaw-tmux-persistent-process
description: >
  Run programs that survive OpenClaw exec session cleanup and gateway restarts via tmux.
  Use when you need long-running servers, dev servers, tunnels (ngrok/cloudflared),
  coding agents, or any process that must outlive the current exec session.
  Solves: exec background processes getting SIGKILL on session cleanup.
  Recommended for all OpenClaw users running any long-lived process.
---

# OpenClaw Tmux Persistent Process

Run programs that survive OpenClaw exec session cleanup and gateway restarts.

## Why every OpenClaw user should have this

OpenClaw runs shell commands via `exec`. But exec has a critical limitation that most users don't realize until something breaks:

- **Background processes are tied to the exec session.** When the session cleans up (idle timeout, context compaction, or gateway restart), all background processes receive SIGKILL and die immediately.
- **Gateway restarts kill everything.** Updates, config changes, or `openclaw gateway restart` — all running exec processes are gone.
- **No warning.** Your tunnel, dev server, or build task just silently disappears.

This means anything you expect to keep running — a tunnel for a client demo, a dev server, a long build — can die at any moment without notice.

**The solution:** Use **tmux** to create virtual terminals completely decoupled from the exec lifecycle. Programs in tmux survive gateway restarts, exec cleanup, and session timeouts. tmux runs independently of OpenClaw — even if the gateway goes down, your processes keep running.

**Rule of thumb:** If a command might run longer than 2 minutes, use tmux.

---

## Socket convention

All operations use a dedicated socket to avoid interfering with the user's own tmux:

```bash
SOCK="/tmp/openclaw-tmux/openclaw.sock"
mkdir -p /tmp/openclaw-tmux
```

## Start a process

```bash
SESSION="my-server"

# Check if already running
if tmux -S "$SOCK" has-session -t "$SESSION" 2>/dev/null; then
  echo "already running"
else
  tmux -S "$SOCK" new -d -s "$SESSION" \
    "cd /path/to/project && npm run dev"
  echo "started"
fi
```

## Monitor

```bash
# List all sessions
tmux -S "$SOCK" list-sessions

# View last 30 lines of output
tmux -S "$SOCK" capture-pane -t "$SESSION" -p -S -30

# Check if process is idle (back to shell prompt)
tmux -S "$SOCK" capture-pane -t "$SESSION" -p -S -3 \
  | grep -qE '\$\s*$|❯' && echo "IDLE" || echo "RUNNING"
```

## Interact

```bash
# Send a command
tmux -S "$SOCK" send-keys -t "$SESSION" "command" Enter

# Send literal text (recommended, no special key parsing)
tmux -S "$SOCK" send-keys -t "$SESSION" -l -- "literal text"
tmux -S "$SOCK" send-keys -t "$SESSION" Enter

# Ctrl+C to interrupt
tmux -S "$SOCK" send-keys -t "$SESSION" C-c
```

## Stop / cleanup

```bash
# Kill one session
tmux -S "$SOCK" kill-session -t "$SESSION"

# Kill all
tmux -S "$SOCK" kill-server

# Clean stale socket
rm -f "$SOCK"
```

## Start interactive programs (wait for ready)

For programs that need startup time (e.g. coding agents, REPLs):

```bash
SESSION="my-task"
tmux -S "$SOCK" new -d -s "$SESSION"
tmux -S "$SOCK" send-keys -t "$SESSION" "cd ~/project && node" Enter

# Wait for prompt before sending commands
for i in $(seq 1 15); do
  OUTPUT=$(tmux -S "$SOCK" capture-pane -t "$SESSION" -p -S -5)
  if echo "$OUTPUT" | grep -qE '❯|>\s*$|ready'; then
    break
  fi
  sleep 1
done

# Now safe to send input
tmux -S "$SOCK" send-keys -t "$SESSION" -l "your command"
tmux -S "$SOCK" send-keys -t "$SESSION" Enter
```

## Common use cases

| Use case | Session name | Command example |
|----------|-------------|-----------------|
| Dev server | `dev-server` | `npm run dev` |
| Tunnel (ngrok) | `tunnel-ngrok` | `ngrok http 3000` |
| Tunnel (localhost.run) | `tunnel-lr` | `ssh -R 80:localhost:3000 nokey@localhost.run` |
| Background worker | `worker` | `python worker.py` |
| Build task | `build-app` | `npm run build` |

## Session naming

Lowercase + hyphens. No spaces.

```
dev-server       — development servers
tunnel-{name}    — tunnels (ngrok, cloudflared, etc.)
build-{project}  — build tasks
worker-{name}    — background workers
```

## Important notes

- **Reboot = gone.** tmux doesn't survive system restarts. Re-create sessions after reboot.
- **Scrollback limit.** Default 2000 lines. Increase with: `tmux set-option -t "$SESSION" history-limit 10000`
- **Socket stale.** If `list-sessions` says "error connecting", delete the socket and recreate.
- **Environment.** tmux inherits env at creation time. Set vars in the command: `tmux new -d -s name "export KEY=val && cmd"`
- **No conflict.** Dedicated socket means zero interference with user's own tmux.

## Requirements

- **tmux 2.6+** (for `send-keys -l` literal mode)
- Check: `tmux -V`
- Install: `brew install tmux` (macOS) or `apt install tmux` (Linux)
