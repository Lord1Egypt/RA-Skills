---
name: occ
description: Control OpenCode to execute development tasks. Provides session management and task execution capabilities.
---

# OCC (OpenCode Controller)

Control OpenCode to execute development tasks via CLI.

## When to Use

Use this skill when:
- You want to delegate coding tasks to OpenCode
- You need to control OpenCode from external systems (like OpenCLAW)
- You want to automate development workflows

## Quick Start

### Prerequisites

OpenCode CLI must be installed and available in PATH.

## Workflow

### Step 1: Choose Working Directory

⚠️ **Important**: Run the script in the directory where you want OpenCode to work. The session will be created in the current directory.

### Step 2: Decide Session Mode

- **New session**: Use `create` command (creates session only, then use `continue` to execute task)
- **Continue existing session**: Use `continue` command (session ID provided by caller)

### Step 3: Run Command

```bash
# Query existing sessions
node skills/occ/scripts/bin/opencode-server.js query

# Create a new session
node skills/occ/scripts/bin/opencode-server.js create "Create a React login page"

# Continue a session
node skills/occ/scripts/bin/opencode-server.js continue <session-id> "Add password reset"
```



## How It Works

The script automatically handles OpenCode Server:

1. **Port Detection**: Scans ports 4096-4200 to find an existing OpenCode Server
2. **Auto-Start**: If no server is found, automatically starts a new one
3. **Session Management**: Creates and manages development sessions through OpenCode's session API



