---
name: kill-tool
description: Terminate processes by sending signals. Use for stopping unresponsive programs, managing background tasks, and process lifecycle control.
---
# Kill - Process Signal Utility

Send termination signals to running processes identified by PID. Supports graceful shutdown (SIGTERM) and forceful termination (SIGKILL).

## Usage

```bash
kill-tool [options] <pid>
```

## Common Signals

- `-15` (SIGTERM): Graceful termination - default
- `-9` (SIGKILL): Force kill - immediate stop
- `-2` (SIGINT): Interrupt - like Ctrl+C
- `-1` (SIGHUP): Hangup - reload config
- `-l`: List all available signal names

## Examples

```bash
# Graceful termination
kill-tool 1234

# Force kill
kill-tool -9 5678

# List all signals
kill-tool -l
```