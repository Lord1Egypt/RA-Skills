---
name: oho
description: OpenCode CLI for submitting coding tasks, managing sessions, and delegating work to coding agents. Use when: (1) submitting coding tasks, (2) creating/managing sessions, (3) delegating work to coding agents, (4) checking task status, (5) configuring OpenCode settings.
---

# OpenCode Server API Skill Handbook

> **Version**: v4.6.0 | **Server**: v1.2.15 | **oho CLI**: v1.1.2
> 
> **⚠️ Important**: All OpenCode operations must be sent via **oho CLI**. Python SDK or curl are no longer supported.

---

## 🚫 Telegram Message Guidelines (Important)

**Prohibited Content**:
- ❌ Do not send notifications like "There are updates", "Skill has been updated"
- ❌ Do not send formatted version changelogs
- ❌ Do not send lengthy confirmation reports after task submission

**Correct Approach**:
- ✅ Return only a concise session ID and status after task submission
- ✅ Notify users only when there is substantial progress
- ✅ Keep messages brief and direct

**Example**:
```
✅ Task submitted
Session: ses_xxx
Project: babylon3DWorld
```

---

## 🚀 Quick Start

### Submit Tasks (Async Mode to Avoid Timeout)

```bash
# Most common: create session + send message in one command, `directory` is the project path
oho add "Fix login bug" --title "Bug Fix" --directory /mnt/d/fe/babylon3DWorld --model "minimax-cn-coding-plan:MiniMax-M2.7" --no-reply

# Another example: summarize today's progress  
oho add "Summarize today's changes" --title "Command Test" --directory /mnt/d/fe/opencode_cli --model "minimax-cn-coding-plan:MiniMax-M2.7" --no-reply

# Specify Agent
oho add "@hephaestus Fix login bug" --title "Bug Fix" --directory /mnt/d/fe/project --model "minimax-cn-coding-plan:MiniMax-M2.7" --no-reply
  
# Attach files
oho add "Analyze logs" --file /var/log/app.log --directory /mnt/d/fe/project --no-reply
```

### Key Parameters

| Parameter | Type | Description | Default |
|------|------|------|--------|
| `--title` | string | Session title (auto-generated if not provided) | Auto-generated |
| `--parent` | string | Parent session ID (for creating child sessions) | - |
| `--directory` | string | Session working directory, project path | Current directory |
| `--agent` | string | Agent ID for the message | - |
| `--model` | string | Model ID for the message (e.g., `provider:model`) | minimax-cn-coding-plan/MiniMax-M2.7 |
| `--no-reply` | bool | Do not wait for AI response | false |
| `--system` | string | System prompt | - |
| `--tools` | string[] | Tool list (can be specified multiple times) | - |
| `--file` | string[] | File attachments (can be specified multiple times) | - |
| `--timeout` | int | Request timeout in seconds | 300 |
| `-j, --json` | bool | JSON output | false |

---

## 📋 Common Commands

### Session Management

```bash
# List all sessions
oho session list

# Filter by ID (fuzzy match)
oho session list --id ses_abc

# Filter by title (fuzzy)
oho session list --title "test"

# Filter by project ID
oho session list --project-id proj1

# Filter by directory
oho session list --directory babylon

# Filter by timestamp
oho session list --created 1773537883643
oho session list --updated 1773538142930

# Filter by status
oho session list --status running    # running/completed/error/aborted/idle
oho session list --running           # Show only running sessions

# Sort and pagination
oho session list --sort updated --order desc  # Sort by updated descending
oho session list --limit 10 --offset 0        # Pagination

# JSON output
oho session list -j

# Create session
oho session create
oho session create --title "name"
oho session create --parent ses_xxx    # Create child session
oho session create --path /path        # Create in specified directory

# Get session details
oho session get <id>

# Update session
oho session update <id> --title "New Title"

# Get child sessions
oho session children <id>

# Get todo items
oho session todo <id>

# Branch session
oho session fork <id>

# Abort session
oho session abort <id>

# Share/unshare session
oho session share <id>
oho session unshare <id>

# Get file diff
oho session diff <id>

# Session summary
oho session summarize <id>

# Revert message
oho session revert <id> --message <msg-id>
oho session unrevert <id>

# Respond to permission request
oho session permissions <id> <perm-id> --response allow

# Delete session
oho session delete ses_xxx

# Archive session
oho session achieve <id> --directory /mnt/d/fe/project
```

### Message Management

```bash
# List messages
oho message list -s ses_xxx

# Get message details
oho message get -s ses_xxx <msg-id>

# Send message (sync)
oho message add -s ses_xxx "Continue task"

# Send async (don't wait for response)
oho message prompt-async -s ses_xxx "Task content"

# Execute command
oho message command -s ses_xxx /help

# Run shell command
oho message shell -s ses_xxx --agent default "ls -la"
```

### Project Management

```bash
# List all projects
oho project list

# Get current project
oho project current

# Get current path
oho path

# Get VCS info
oho vcs

# Dispose current instance
oho instance dispose
```

### Global Commands

```bash
# Check server health
oho global health

# Listen to global event stream (SSE)
oho global event
```

### Configuration Management

```bash
# Get configuration
oho config get

# Update configuration
oho config set --theme dark

# List providers
oho config providers
```

### Provider Management

```bash
# List all providers
oho provider list

# Get authentication methods
oho provider auth

# OAuth authorization
oho provider oauth authorize <id>

# Handle callback
oho provider oauth callback <id>
```

### File Operations

```bash
# List files
oho file list [path]

# Read file content
oho file content <path>

# Get file status
oho file status
```

### Find Commands

```bash
# Search text
oho find text "pattern"

# Find files
oho find file "query"

# Find symbols
oho find symbol "query"
```

### Other Commands

```bash
# List agents
oho agent list

# List commands
oho command list

# List tool IDs
oho tool ids

# List tools
oho tool list --provider xxx --model xxx

# LSP status
oho lsp status

# Formatter status
oho formatter status

# MCP servers
oho mcp list
oho mcp add <name> --config '{}'

# TUI
oho tui open-help
oho tui show-toast --message "message"

# Auth setup
oho auth set <provider> --credentials key=value
```

---

## ⚠️ Timeout Handling (Important)

The `oho add` command waits for AI response by default. For complex tasks, the AI may need more time to think, which could cause timeout.

### Ways to Avoid Timeout

**Method 1: Use `--no-reply` Parameter** (Recommended)
```bash
# ✅ Returns immediately after sending message, no waiting for AI response
oho add "Analyze project structure" --directory /mnt/d/fe/project --no-reply

# Check results later
oho message list -s <session-id>
```

**Method 2: Increase Timeout**
```bash
# Set timeout to 10 minutes (600 seconds)
export OPENCODE_CLIENT_TIMEOUT=600
oho add "Complex task" --directory /mnt/d/fe/project

# Or set temporarily
OPENCODE_CLIENT_TIMEOUT=600 oho add "Complex task" --directory /mnt/d/fe/project
```

**Method 3: Use `--timeout` Parameter** (Most Convenient)
```bash
# Temporarily set timeout to 10 minutes
oho add "Complex task" --directory /mnt/d/fe/project --timeout 600

# Set timeout to 1 hour
oho add "Large refactor" --directory /mnt/d/fe/project --timeout 3600
```

**Method 4: Use Async Commands**
```bash
# Create session first
oho session create --title "task" --path /mnt/d/fe/project

# Send message async
oho message prompt-async -s <session-id> "Task description"
```

### Timeout Configuration

| Configuration Method | Priority | Description |
|----------|--------|-------------|
| `--timeout` parameter | Highest | Temporary override, only effective for current command |
| `OPENCODE_CLIENT_TIMEOUT` env var | Medium | Effective for current shell session |
| Default value | Lowest | 300 seconds (5 minutes) |

### Timeout Error Messages

If timeout occurs, you will see a friendly error:
```
Request timeout (300 seconds)

Suggestions:
  1. Use --no-reply parameter to avoid waiting
  2. Increase timeout via env var: export OPENCODE_CLIENT_TIMEOUT=600
  3. Use async command: oho message prompt-async -s <session-id> "task"
```

### Background Polling (Optional)

```bash
#!/bin/bash
session_id=$(oho add "task" --directory /mnt/d/fe/project --json | jq -r '.sessionId')

while true; do
    count=$(oho message list -s "$session_id" -j | jq 'length')
    [ "$count" -ge 2 ] && echo "✅ Done" && break
    echo "⏳ Running... ($count messages)"
    sleep 10
done
```

---

## 🤖 Agent System

| Agent | Role | Use Cases |
|-------|------|---------|
| **@sisyphus** | Main coordinator | Large feature development, parallel execution |
| **@hephaestus** | Deep worker | Code exploration, performance optimization |
| **@prometheus** | Strategic planner | Requirements clarification, architecture design |

---

## 📝 Practical Examples

### babylon3DWorld Project Tasks

```bash
#!/bin/bash
# Submit coding task

oho add "@hephaestus ulw optimize navigation logic between editor and world pages

**Coding Goals**:
1. When returning from editor to world page: refresh directly, no longer check if editor made changes
2. When entering editor from world page: no longer cache the world itself

**Keywords**: ulw" \
  --directory /mnt/d/fe/babylon3DWorld \
  --title "ulw - Optimize editor navigation logic" \
  --no-reply

echo "✅ Task submitted"
```

### Multi-Project Batch Tasks

```bash
#!/bin/bash
# Batch submit tasks

oho add "Task 1" --directory /mnt/d/fe/babylon3DWorld --no-reply
oho add "Task 2" --directory /mnt/d/fe/wujimanager --no-reply
oho add "Task 3" --directory /mnt/d/fe/armdraw --no-reply

echo "✅ All tasks submitted"
```

---

# OpenCode Server Usage

1. rerun.sh

```
#!/bin/bash

echo "🔴 stopping opencode web service..."
pkill -f "opencode web"
sleep 2


if pgrep -f "opencode web" > /dev/null; then
    pkill -9 -f "opencode web"
    sleep 1
fi

echo "✅ opencode web stopped"
echo "🟢 starting opencode web service..."
bash run.sh &

echo "✅ opencode web started"
```

2. run.sh

```
OPENCODE_SERVER_PASSWORD=cs516123456 opencode web --hostname 0.0.0.0  --port 4096 --mdns --mdns-domain opencode.local
```

    

 

## 🔧 Troubleshooting

### Restart OpenCode Server

**Standard Restart** (Recommended):
```bash
# Switch to project directory and run restart script
cd /mnt/d/fe && bash rerun.sh &
```

**Description**:

- `rerun.sh` automatically stops old service and starts new one
- Use `&` to run in background to avoid blocking
- Wait 3-5 seconds after restart for service to fully start

**Verify Service is Running**:
```bash
# Wait for service to start
sleep 5

# Check processes
ps aux | grep "opencode web"

# Test API
oho session list
```

**View Logs**:
```bash
# View run.sh output logs
tail -f /tmp/opencode.log

# Or view recent logs
tail -50 /tmp/opencode.log
```

**If Restart Script Gets Stuck**:
```bash
# Force kill stuck process
pkill -9 -f "bash rerun.sh"

# Manual restart
cd /mnt/d/fe
pkill -f "opencode web"
sleep 2
OPENCODE_SERVER_PASSWORD=yourpassword opencode web --hostname 0.0.0.0 --port 4096 --mdns --mdns-domain opencode.local &
```

### 401 Unauthorized
```bash
# Check password
echo $OPENCODE_SERVER_PASSWORD

# Or specify via command line
oho --password yourpassword session list
```

### Session Not Found
```bash
# Recreate session
oho session create --path /mnt/d/fe/babylon3DWorld
```

### Task Timeout
```bash
# Use --no-reply to submit async
oho add "task" --directory /mnt/d/fe/project --no-reply
```

### ConfigInvalidError (500 Error)

**Symptoms**:
```bash
Error: API Error [500]: {"name":"ConfigInvalidError","data":{"path":"/path/to/project/.opencode/opencode.json","issues":[...]}}
```

**Cause**:
The `opencode.json` or `.opencode/opencode.json` config file in the project does not comply with the schema requirements.

**Common Errors**:
```json
// ❌ Wrong: tools.lint should be boolean, not object
{
  "tools": {
    "lint": {
      "type": "shell",
      "command": ["yarn", "lint"]
    }
  }
}

// ❌ Wrong: lsp config format is incorrect
{
  "lsp": {
    "vue": {
      "disabled": false  // Should be true/false, but schema expects different format
    }
  }
}
```

**Solution**:
```bash
# 1. Backup incorrect config file
mv opencode.json opencode.json.bak
mv .opencode/opencode.json .opencode/opencode.json.bak

# 2. Restart opencode server (using rerun.sh)
cd /mnt/d/fe && bash rerun.sh &

# 3. Verify service is running
sleep 5
oho session list

# 4. If you need config, use correct format
cat > .opencode/opencode.json << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "model": "alibaba-cn/qwen3.5-plus"
}
EOF
```

**Prevention**:
- Backup `opencode.json` before modifying
- Use `oho config get` to verify config is valid
- Reference official schema: https://opencode.ai/config.json

---

## 🔗 MCP Server

oho can act as an MCP (Model Context Protocol) server, allowing external MCP clients (like Claude Desktop, Cursor, etc.) to call OpenCode API via MCP protocol.

### Start MCP Server

```bash
# Start MCP server (stdio mode)
oho mcpserver
```

### Available MCP Tools

| Tool | Description |
|------|------|
| `session_list` | List all sessions |
| `session_create` | Create new session |
| `session_get` | Get session details |
| `session_delete` | Delete session |
| `session_status` | Get all session statuses |
| `message_list` | List messages in session |
| `message_add` | Send message to session |
| `config_get` | Get OpenCode configuration |
| `project_list` | List all projects |
| `project_current` | Get current project |
| `provider_list` | List AI providers |
| `file_list` | List files in directory |
| `file_content` | Read file content |
| `find_text` | Search text in project |
| `find_file` | Find files by name |
| `global_health` | Check server health status |

### MCP Client Configuration

#### Claude Desktop (macOS/Windows)

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "oho": {
      "command": "oho",
      "args": ["mcpserver"],
      "env": {
        "OPENCODE_SERVER_HOST": "127.0.0.1",
        "OPENCODE_SERVER_PORT": "4096",
        "OPENCODE_SERVER_PASSWORD": "your-password"
      }
    }
  }
}
```

#### Cursor

Add to Cursor settings (JSON mode):

```json
{
  "mcpServers": {
    "oho": {
      "command": "oho",
      "args": ["mcpserver"],
      "env": {
        "OPENCODE_SERVER_HOST": "127.0.0.1",
        "OPENCODE_SERVER_PORT": "4096",
        "OPENCODE_SERVER_PASSWORD": "your-password"
      }
    }
  }
}
```

---

## 🔗 Related Resources

- **OpenCode Official Docs**: https://opencode.ai/docs/
- **oho CLI Repository**: https://github.com/tornado404/opencode_cli
- **OpenAPI Spec**: http://localhost:4096/doc

---

*Created: 2026-02-27 13:46 CST*  
*Last Updated: 2026-04-02 00:43 CST - Added session achieve command*
