---
name: openclaw-claudecode
description: |
  Control Claude Code (cc) via tmux to execute development tasks. Use for: starting CC development sessions, sending development commands, monitoring progress, auto-confirming prompts.
  Trigger: user requests "start CC development", "use Claude Code to develop", "tmux + cc to execute task", "monitor CC progress", "check CC output".
  Not for: simple code edits (use edit tool directly), non-development Claude conversations.
metadata:
  author: FlorianFan
  version: "1.1.0"
---

# openclaw-claudecode Skill

Control Claude Code through tmux sessions for long-running development tasks.

## Environment Check & Initialization (Required for First Use)

### 0.1 Check tmux

```bash
# Check if tmux is installed
which tmux || echo "tmux not found"

# If not installed, install tmux
# CentOS/RHEL/Rocky:
dnf install -y tmux || yum install -y tmux

# Ubuntu/Debian:
apt install -y tmux

# Alpine:
apk add tmux
```

### 0.2 Check Claude Code

```bash
# Check if claude command is available
which claude || echo "claude not found"

# If not installed, install Claude Code
npm install -g @anthropic-ai/claude-code

# Or use official install script
curl -fsSL https://claude.ai/install.sh | sh
```

### 0.3 Verify Claude Code Works

```bash
# Check version
claude --version

# Test simple call (requires valid authentication)
claude --print "hello" 2>&1 | head -5
```

**Common Issues**:
- `Not logged in` → Run `claude /login` first or configure `ANTHROPIC_API_KEY`
- `model not found` → Check if API endpoint supports the specified model

### 0.4 Create Regular User (CC refuses root)

```bash
# Check if regular user exists
id <username> || echo "user not found"

# Create user (if not exists)
useradd -m -s /bin/bash <username>

# Set password (optional)
echo "<username>:<password>" | chpasswd
```

**Recommended usernames**: `claudecode`, `developer`, `ccdev`

### 0.5 Environment Check Summary

Run complete environment check:

```bash
# One-click check script
check_env() {
  echo "=== tmux ==="
  which tmux && tmux -V || echo "❌ tmux missing"

  echo "=== claude ==="
  which claude && claude --version || echo "❌ claude missing"

  echo "=== user ==="
  id <username> || echo "❌ user missing"

  echo "=== auth ==="
  claude --print "test" 2>&1 | grep -E "error|Error" && echo "❌ auth failed" || echo "✅ auth ok"
}
check_env
```

**All checks must pass before proceeding**

---

## Core Flow

### 1. Locate Project Directory

```bash
# Check directory exists
ls -la <project_path>

# Check if it's a git repo (CC requires)
ls -la <project_path>/.git
```

**Directory not found → Immediately ask user to confirm path**

### 2. Create tmux Session

```bash
# Create session (with working directory)
tmux new-session -d -s <session_name> -c <project_path>

# Verify session
tmux list-sessions
```

**Session naming suggestion**: `cc-<project>` or `claude-<task>`

### 3. Switch User + Start CC

CC refuses root, must switch to regular user:

```bash
# Send command: switch user + cd + start CC
tmux send-keys -t <session_name> "su - <username> -c 'cd <project_path> && claude --dangerously-skip-permissions'" Enter
```

**Key Parameters**:
- `--dangerously-skip-permissions`: Skip all confirmation prompts, fully automatic
- `--print`: Silent mode, buffer output until complete (for background tasks)

### 4. Send Development Commands

```bash
# Single line command
tmux send-keys -t <session_name> "<prompt>" Enter

# Multi-line command (use load-buffer)
cat << 'EOF' | tmux load-buffer -
First line
Second line
Third line
EOF
tmux paste-buffer -t <session_name>
tmux send-keys -t <session_name> Enter
```

### 5. Monitor Progress

```bash
# View recent output
tmux capture-pane -t <session_name> -p | tail -30

# View full scroll history
tmux capture-pane -t <session_name> -p -S -

# Check if input is needed
tmux capture-pane -t <session_name> -p | tail -10 | grep -E "❯|Yes.*No|proceed|permission|y/n"
```

### 6. Auto-confirm/Interact

```bash
# Send confirmation
tmux send-keys -t <session_name> y Enter

# Send cancel
tmux send-keys -t <session_name> n Enter

# Send Ctrl+C interrupt
tmux send-keys -t <session_name> C-c
```

---

## Complete Example

### Start Development Task (with Environment Check)

```bash
# 0. Environment check
which tmux || dnf install -y tmux
which claude || npm install -g @anthropic-ai/claude-code
id claudecode || useradd -m claudecode

# 1. Create session
tmux new-session -d -s cc-<project> -c <project_path>

# 2. Start CC (regular user)
tmux send-keys -t cc-<project> "su - claudecode -c 'cd <project_path> && claude --dangerously-skip-permissions'" Enter

# 3. Wait for CC to start (~5 seconds)
sleep 5

# 4. Send development task
tmux send-keys -t cc-<project> "<prompt>" Enter

# 5. Monitor progress
tmux capture-pane -t cc-<project> -p | tail -20
```

### Check CC Process Status

```bash
# Check if CC is running
ps aux | grep -i claude | grep -v grep

# Check runtime duration
ps -o pid,etime,cmd -p $(pgrep -f "claude --dangerously")
```

### Session Management

```bash
# List all sessions
tmux list-sessions

# List all attach clients
tmux list-clients

# Attach to session (interactive view)
tmux attach -t <session_name>

# Kill session
tmux kill-session -t <session_name>

# Kill other attach clients (keep yours)
tmux detach-client -t <session_name> -a

# Detach from attached session
# Shortcut: Ctrl+B then D
```

---

## Common Issues

### CC Refuses Root

**Solution**: Switch to non-root user

```bash
tmux send-keys -t <session_name> "su - <username> -c 'cd <project_path> && claude --dangerously-skip-permissions'" Enter
```

### 504 Gateway Timeout

**Cause**: Claude API server temporary error

**Solution**: Wait 1-2 minutes then restart CC

```bash
# Interrupt current process
tmux send-keys -t <session_name> C-c

# Restart
tmux send-keys -t <session_name> "claude --dangerously-skip-permissions" Enter
```

### CC Stuck at Confirmation Prompt

**Detection**:

```bash
tmux capture-pane -t <session_name> -p | tail -5 | grep -E "y/n|Yes|No|proceed"
```

**Solution**:

```bash
tmux send-keys -t <session_name> y Enter
```

### Attach Processes Residue

**Detection**:

```bash
tmux list-clients
ps aux | grep "tmux attach" | grep -v grep
```

**Cleanup**:

```bash
# Kill extra attach processes
kill <PID1> <PID2>

# Or kick other clients
tmux detach-client -t <session_name> -a
```

### Check CC Completion Status

```bash
# Check if back to shell prompt
tmux capture-pane -t <session_name> -p | tail -3 | grep -E "\\$|#|❯"

# Check git commits
cd <project_path> && git log --oneline -3
```

---

## Best Practices

1. **Must check environment on first use**: tmux, claude, regular user, authentication
2. **Clear session naming**: `cc-<project>-<task>` for managing multiple tasks
3. **Regular progress check**: Use `capture-pane` every 30 minutes
4. **Record session ID**: Note session name and start time in memory file
5. **Clean residual attach**: Regularly check `tmux list-clients` and cleanup

---

## Command Reference

| Command | Purpose |
|---------|---------|
| `tmux new-session -d -s NAME -c DIR` | Create background session |
| `tmux send-keys -t NAME "CMD" Enter` | Send command |
| `tmux capture-pane -t NAME -p` | Capture output |
| `tmux capture-pane -t NAME -p -S -` | Capture full history |
| `tmux list-sessions` | List sessions |
| `tmux list-clients` | List attach clients |
| `tmux kill-session -t NAME` | Kill session |
| `tmux attach -t NAME` | Attach session |
| `tmux detach-client -t NAME -a` | Kick other clients |
| `tmux send-keys -t NAME C-c` | Send Ctrl+C |
| `tmux send-keys -t NAME y Enter` | Send confirmation |
| `tmux send-keys -t NAME n Enter` | Send cancel |

| Check Command | Purpose |
|---------------|---------|
| `which tmux` | Check tmux |
| `which claude` | Check claude |
| `claude --version` | Check version |
| `id <user>` | Check user exists |
| `ps aux | grep claude` | Check process |