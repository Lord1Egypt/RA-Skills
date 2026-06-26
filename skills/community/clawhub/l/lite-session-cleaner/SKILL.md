---
name: session-cleaner
description: Automatically cleans up inactive sessions (older than 1 hour) and sends a notification.
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["openclaw"] }
    }
  }
---

# Session Cleaner Skill

This skill is designed to be run via a cron job or periodic task to monitor and prune stale sessions.

## Usage

The skill relies on `openclaw sessions_list` to identify old sessions and `openclaw sessions_kill` to terminate them. It can be integrated into a TaskFlow or run as a standalone script via `exec`.

## Implementation Logic

1. **Identify**: Use `sessions_list` to retrieve all active sessions.
2. **Filter**: Compare the `last_activity` timestamp of each session with the current time.
3. **Action**: For sessions where `current_time - last_activity > 3600` seconds:
    - Send a message to the session's target channel (e.g., via `message` tool) stating: "当前会话已经结束".
    - Execute `sessions_kill <session_id>`.
4. **Log**: Record the cleaning action in the daily log.

## Requirements

- `openclaw` CLI installed and accessible.
- Access to session metadata.
