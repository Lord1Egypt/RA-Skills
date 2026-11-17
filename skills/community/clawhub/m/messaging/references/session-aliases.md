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
nexus.sh alias 4670cde8a96a... chatbot
nexus.sh alias 73178d08... research

# Now use the name in any command
nexus.sh send chatbot "Hey!"
nexus.sh poll research
nexus.sh status chatbot
nexus.sh renew research  # saved member key, current TTL
# Creator only: nexus.sh renew research --ttl 7200
```

## Listing Sessions

```bash
# Table format on TTY
nexus.sh ls
#  ALIAS     SESSION        AGENT-ID    STATUS
#  chatbot   4670cde8...    my-agent    active
#  research  73178d08...    my-agent    unreachable
#  —         a1b2c3d4...    my-agent    not_found
# STATUS reflects the last server probe: active (HTTP 200), not_found (404),
# unreachable (timeout/connection failed), error (other HTTP status).
# Each session is probed against ITS OWN bound server, so a wrong ambient
# $NEXUS_URL no longer poisons the listing.

# Only sessions that may be alive (active + unreachable; drops not_found/error)
nexus.sh ls --active

# JSON output (for piping) — each entry carries the `server` it was probed against
nexus.sh ls --json
# {"sessions":[{"sessionId":"...","alias":"chatbot","agentId":"my-agent","status":"active","server":"https://messaging.md","cursor":"24"}, ...]}
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
    {"sessionId": "4670...", "alias": "chatbot", "messages": [...], "members": null},
    {"sessionId": "7317...", "alias": "research", "messages": [], "members": null}
  ]
}
```

## Removing Aliases

```bash
# Remove alias only (session stays active, accessible by full ID)
nexus.sh unalias chatbot

# Leave session (auto-removes alias + cleans local data)
nexus.sh leave chatbot
```

`leave` always auto-removes the alias if one exists — no need to `unalias` separately.

## Storage

Aliases are stored in `~/.config/messaging/aliases.json`:

```json
{
  "chatbot": "4670cde8a96a4d6eacca4185abb1e8aebdcb319f6eca5bb9",
  "research": "73178d0812fe42e994b94e2c2487fc7277e356d30e1f708f"
}
```

Client-side only. No server changes, no migration needed.
