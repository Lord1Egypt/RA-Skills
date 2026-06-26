---
name: BashTool
description: "Execute shell commands with background continuation. Use for running system commands, scripts, and CLI tools. Supports PTY for TTY-required commands."
metadata: { "openclaw": { "emoji": "💻", "requires": { "bins": ["bash"] } } }
---

# BashTool

Execute shell commands with full control over execution.

## When to Use

✅ **USE this skill when:**
- Running system commands
- Executing scripts
- Installing packages
- Managing files and directories
- Running Git operations
- Starting background processes

❌ **DON'T use this skill when:**
- Simple file reads → use `FileReadTool`
- Simple file writes → use `FileWriteTool`
- Precise text edits → use `FileEditTool`

## Usage

```bash
# Simple command
exec --command "ls -la"

# Command with working directory
exec --command "git status" --workdir /path/to/repo

# Command with environment variables
exec --command "echo $HOME" --env '{"MY_VAR": "value"}'

# Background process
exec --command "npm start" --background true

# PTY for interactive commands
exec --command "vim file.txt" --pty true
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `command` | string | Shell command to execute (required) |
| `workdir` | string | Working directory (defaults to cwd) |
| `env` | object | Environment variables |
| `yieldMs` | number | Milliseconds to wait before backgrounding |
| `background` | boolean | Run in background immediately |
| `timeout` | number | Timeout in seconds |
| `pty` | boolean | Run in pseudo-terminal (for TTY-required CLIs) |
| `elevated` | boolean | Run with elevated permissions |
| `host` | string | Exec host (sandbox|gateway|node) |
| `security` | string | Exec security mode (deny|allowlist|full) |

## Examples

### Example 1: Run Git Commands

```bash
exec --command "git log --oneline -5"
exec --command "git status"
exec --command "git add . && git commit -m 'Update'"
```

### Example 2: Install Dependencies

```bash
exec --command "npm install"
exec --command "pip install -r requirements.txt"
```

### Example 3: Run Tests

```bash
exec --command "npm test"
exec --command "pytest tests/"
```

### Example 4: Background Process

```bash
# Start a server in background
exec --command "npm start" --background true --yieldMs 5000
```

### Example 5: PTY for Interactive CLI

```bash
# Commands requiring TTY
exec --command "htop" --pty true
exec --command "vim file.txt" --pty true
```

## Process Management

For background processes, use the `process` tool:

```bash
# List running processes
process --action list

# Poll process output
process --action poll --sessionId <id> --timeout 5000

# Get process logs
process --action log --sessionId <id>

# Kill process
process --action kill --sessionId <id>
```

## Security Notes

⚠️ **Command execution risks:**
- Commands run with your user permissions
- Elevated mode requires explicit approval
- Destructive commands (rm, etc.) need caution
- Network operations may be restricted

## Best Practices

1. **Use specific paths**: Avoid relying on PATH for critical commands
2. **Quote variables**: Prevent shell injection
3. **Check exit codes**: Verify command success
4. **Use timeouts**: Prevent hanging processes
5. **Log output**: Capture command output for debugging

## Integration Notes

This is a core OpenClaw built-in tool. No additional setup required.
