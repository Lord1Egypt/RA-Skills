---
name: neckr0ik-session-healer
version: 1.0.0
description: Automatically detects and heals locked OpenClaw session files. Use when you see "session file locked" errors or models failing due to lock timeouts. Clears stale locks and recovers failed sessions.
---

# Session Healer

Automatically detects and heals locked OpenClaw session files.

## Quick Start

```bash
# Check for locked sessions
neckr0ik-session-healer check

# Clear all stale locks
neckr0ik-session-healer heal

# Clear specific session lock
neckr0ik-session-healer unlock <session-id>
```

## What This Fixes

The "session file locked" error occurs when:
- OpenClaw crashes while writing to a session
- Multiple processes try to access the same session
- Network timeout during session write
- System crash leaves stale lock files

**Symptoms:**
- "session file locked (timeout 10000ms)" errors
- All models fail with lock timeout
- Session becomes unresponsive

## How It Works

1. Scans `~/.openclaw/agents/*/sessions/*.jsonl.lock` files
2. Checks if the owning process is still alive
3. If process is dead, removes the stale lock
4. Optionally recovers session data if corrupted

## Commands

### check

```bash
neckr0ik-session-healer check [--verbose]

Scans for locked sessions and reports:
- Lock file path
- Owning PID
- Process status (alive/dead)
- Lock age
- Session ID
```

### heal

```bash
neckr0ik-session-healer heal [--force]

Clears all stale locks (where owning process is dead).

Options:
  --force    Clear all locks, even for alive processes (dangerous)
  --dry-run  Show what would be cleared without doing it
```

### unlock

```bash
neckr0ik-session-healer unlock <session-id>

Clears a specific session lock by session ID.
```

### recover

```bash
neckr0ik-session-healer recover <session-id>

Attempts to recover a corrupted session file:
- Validates JSON lines
- Removes corrupted lines
- Creates backup before recovery
```

## Safety Features

- Never clears locks for processes that are still alive (unless --force)
- Creates backups before modifying session files
- Logs all actions for audit trail
- Validates session file integrity after healing

## Example Output

```
$ neckr0ik-session-healer check

Checking for locked sessions...
Found 3 lock files:

  ✗ session: c4fa26e6-20be-4843-9678-a2f328dd1844
    Lock: /Users/user/.openclaw/agents/main/sessions/.../c4fa...jsonl.lock
    PID: 52251 (DEAD - process not running)
    Age: 2 hours 34 minutes
    Status: STALE - safe to clear

  ✓ session: a1b2c3d4-5678-90ab-cdef-1234567890ab
    Lock: /Users/user/.openclaw/agents/main/sessions/.../a1b2...jsonl.lock
    PID: 12345 (ALIVE)
    Age: 5 minutes
    Status: ACTIVE - do not clear

$ neckr0ik-session-healer heal

Healing stale locks...
[CLEARED] c4fa26e6-20be-4843-9678-a2f328dd1844 (PID 52251 was dead)
[SKIPPED] a1b2c3d4-5678-90ab-cdef-1234567890ab (PID 12345 still alive)

Healed 1 session. 0 errors.
```

## See Also

- `scripts/healer.py` - Main healer script
- `references/lock-recovery.md` - Detailed recovery guide