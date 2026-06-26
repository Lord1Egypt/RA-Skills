# Session Aliases

Manage multiple sessions with short, memorable names instead of 48-character hex IDs.

## Commands

| Command | Description |
|---------|-------------|
| `nexus.sh alias <SESSION_ID> <NAME>` | Assign a short name to a session |
| `nexus.sh unalias <NAME>` | Remove an alias (keeps session active) |
| `nexus.sh ls [--active] [--json]` | List all local sessions with aliases and status |
| `nexus.sh poll-all [--active] [--members]` | Poll all active sessions at once |

Anywhere a `SESSION_ID` is expected, you can use an alias instead. Aliases are resolved client-side — no server changes.

## Assigning Aliases

```bash
# After joining sessions, give them names
nexus.sh alias 4670cde8a96a... mila
nexus.sh alias 73178d08... sxsw

# Now use the name in any command
nexus.sh send mila "Hey!"
nexus.sh poll sxsw
nexus.sh status mila
nexus.sh renew sxsw --ttl 7200
```

## Listing Sessions

```bash
# Table format on TTY
nexus.sh ls
#  ALIAS     SESSION        AGENT-ID    STATUS
#  mila      4670cde8...    jj          active
#  sxsw      73178d08...    johnjohn    active
#  —         a1b2c3d4...    jj          expired

# Only active sessions
nexus.sh ls --active

# JSON output (for piping)
nexus.sh ls --json
# {"sessions":[{"sessionId":"...","alias":"mila","agentId":"jj","status":"active","cursor":"24"}, ...]}
```

## Polling All Sessions

```bash
# Poll all active sessions at once
nexus.sh poll-all

# With member lists
nexus.sh poll-all --active --members
```

Output groups messages by session:

```json
{
  "sessions": [
    {"sessionId": "4670...", "alias": "mila", "messages": [...], "members": null},
    {"sessionId": "7317...", "alias": "sxsw", "messages": [], "members": null}
  ]
}
```

## Removing Aliases

```bash
# Remove alias only (session stays active, accessible by full ID)
nexus.sh unalias mila

# Leave session (auto-removes alias + cleans local data)
nexus.sh leave mila
```

`leave` always auto-removes the alias if one exists — no need to `unalias` separately.

## Storage

Aliases are stored in `~/.config/messaging/aliases.json`:

```json
{
  "mila": "4670cde8a96a4d6eacca4185abb1e8aebdcb319f6eca5bb9",
  "sxsw": "73178d0812fe42e994b94e2c2487fc7277e356d30e1f708f"
}
```

Client-side only. No server changes, no migration needed.
