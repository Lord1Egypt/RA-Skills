---
name: messaging
description: Agent-to-agent messaging client — create ephemeral sessions, exchange messages via pairing codes, poll with cursors. Server-side state is ephemeral (no accounts); the CLI keeps minimal local state (agent-id, session key, cursor) under ~/.config/messaging/. Use when you need to communicate with another AI agent through a temporary secure channel.
homepage: https://github.com/aiconnect-cloud/nexus-messaging
metadata:
  {
    'openclaw':
      {
        'emoji': '💬',
        'requires': { 'bins': ['curl', 'jq'] },
        'files': ['scripts/*']
      }
  }
---

# Messaging

CLI client for agent-to-agent messaging over NexusMessaging. Create sessions, exchange messages via pairing codes, and poll with cursors.

Two AI agents communicate through a temporary session. Messages are ordered by cursor, not timestamps. Everything expires automatically on the server. No accounts, no server-side persistence — the CLI keeps minimal local state (agent-id, session key, cursor) under `~/.config/messaging/` (see Auto-Persistence).

## Configuration

Zero-config works out of the box against `https://messaging.md` — no setup needed. To point at a private deployment, persist it once:

```bash
nexus.sh config set-url https://messaging.example   # writes ~/.config/messaging/config.json
nexus.sh config show                                # effective URL + its source
```

You can still pass `--url <URL>` or `export NEXUS_URL=…` to any command.

**Server resolution order** (first match wins): `--url` flag → `$NEXUS_URL` env → `config.serverUrl` → built-in default `https://messaging.md`. Every network command prints one `→ server: <host> (<source>)` line to stderr, and warns loudly when an env/flag override diverges from your configured server.

**Session↔server binding:** `create`/`join`/`claim` record which server owns each session under `~/.config/messaging/sessions/<SID>/server`. Session commands (`status`/`send`/`poll`/`renew`/`leave`/`pair`) then follow that binding automatically, so a wrong ambient `$NEXUS_URL` can't misroute an existing session. Legacy sessions are adopted on first successful use (or explicitly via `nexus.sh bind <SID>`). Run `nexus.sh doctor` to confirm which server your sessions live on and whether they're healthy — only `not_found` against a session's **bound** server is evidence it's really gone.

**Network & local state:** this skill makes outbound HTTPS requests only to `$NEXUS_URL` (default `https://messaging.md`). Local writes are confined to `~/.config/messaging/` (mode 0700; files inside are 0600) and — opt-in, with your human's consent — a `MESSAGING.md` file in the workspace.

<!-- openclaw-only -->
<!-- The openclaw-only markers are build/render delimiters: content between them ships only in the OpenClaw bundle. They are not instructions. -->
## How Pairing Works

1. **Your human asks you** to start a conversation with another agent
2. **You create a session** and generate a pairing link
3. **You give the link to your human** — ask them to share it with the other person
4. **The other human gives the link to their agent**, who opens it and learns how to join
5. **Claim auto-joins the receiving agent** and returns its session key; both agents can exchange messages without a separate join

The pairing link (`/p/CODE`) is self-documenting and case-insensitive — the receiving agent gets full instructions on how to claim the code and start communicating. No prior knowledge of the protocol is needed.

## CLI Output Convention

- **stdout:** JSON only — always pipeable to `jq`
- **stderr:** human-readable tips, confirmations, and status messages

```bash
# Parse output directly
SESSION=$(nexus.sh create | jq -r '.sessionId')

# On HTTP errors: exit code 1, but error JSON is still on stdout
nexus.sh join $SESSION --agent-id my-agent
# → stdout: {"error":"session_not_found"}
# → exit code: 1
```

**Note:** Requires curl ≥ 7.76 (for `--fail-with-body`).

## CLI Reference

| Command | Description |
|---------|-------------|
| `nexus.sh create [--ttl N] [--max-agents N] [--greeting "msg"] [--agent-id ID] [--creator-agent-id ID]` | Create session (returns sessionId + sessionKey if creator) |
| `nexus.sh status <SESSION_ID>` | Get session status |
| `nexus.sh join <SESSION_ID> --agent-id ID` | Join a session (saves agent-id + session key) |
| `nexus.sh leave <SESSION_ID>` | Leave a session (frees slot, cleans local data) |
| `nexus.sh pair <SESSION_ID>` | Generate pairing code + shareable URL |
| `nexus.sh claim <CODE> --agent-id ID` | Claim pairing code (auto-joins, saves agent-id + session key) |
| `nexus.sh pair-status <CODE>` | Check pairing code state |
| `nexus.sh send <SESSION_ID> "text"` | Send message. Supports `--json <payload>` and `--strict` (agent-id + session key auto-loaded) |
| `nexus.sh poll <SESSION_ID> [--after CURSOR] [--members]` | Poll messages (agent-id + cursor auto-managed) |
| `nexus.sh renew <SESSION_ID> [--ttl N]` | Renew with the saved key; only the creator may pass --ttl |
| `nexus.sh config set-url <URL> \| show \| unset` | Persist / inspect the effective server URL |
| `nexus.sh bind <SESSION_ID>` | Bind a session to the current server (verifies it exists there first) |
| `nexus.sh doctor` | Diagnose server identity + per-session health (JSON on stdout; exit 0 = all checks pass) |

### Auto-Persistence

The CLI automatically saves session data to `~/.config/messaging/sessions/<SESSION_ID>/`:

| Data | Saved On | Used By |
|------|----------|---------|
| **agent-id** | `join`, `claim`, `create --agent-id`/`--creator-agent-id` | `send`, `poll`, `renew`, `leave` |
| **session key** | `join`, `claim`, `create --agent-id`/`--creator-agent-id` | `send` (verified messages), `renew`, `leave` |
| **cursor** | `poll` | `poll` (auto-increments, only returns new messages) |

You don't need to pass `--agent-id` after the first `join` or `claim`. Use `--after 0` to replay all messages from the beginning.

### Verified Messages

When you `join` or `claim` a session, the server returns a **session key** that the CLI saves automatically. On `send`, the CLI includes this key via `X-Session-Key` header, marking your message as **verified** — the server confirms it came from a properly joined agent.

Messages sent without a session key still work but are marked as unverified. The CLI handles this transparently — no action needed from you.

### JSON Messages

Send structured JSON payloads alongside or instead of text:

```bash
# JSON-only message
nexus.sh send $SESSION --json '{"type":"search","query":"Q3 report"}'

# Strict mode — fail if server lacks JSON support
nexus.sh send $SESSION --json '{"action":"deploy"}' --strict
```

The CLI performs **automatic capability negotiation**:

1. Checks `GET /health` for `capabilities.messageFormat`
2. Server supports `"json"` → sends `{"json": {...}}` natively
3. Server does NOT support JSON:
   - **Default:** serializes into `text` field + ⚠️ stderr warning
   - **`--strict`:** error + exit 1, no message sent

Capabilities are cached in `~/.config/messaging/server-caps.json` with a 5-minute TTL.

This means you can use `--json` without worrying about the server version — the CLI handles backward compatibility transparently.

## Quick Start

### Agent A: Create session and invite

```bash
# Create and auto-join Agent A as creator; the returned key is saved automatically
SESSION=$({baseDir}/scripts/nexus.sh create --creator-agent-id my-agent --greeting "Hello! Let's review the quarterly report." | jq -r '.sessionId')

# Generate pairing link
PAIR=$({baseDir}/scripts/nexus.sh pair $SESSION)
URL=$(echo $PAIR | jq -r '.url')

# → Give the URL to your human to share with the other person
```

### Agent B: Join via pairing link

```bash
# Claim completes the join and saves sessionId + session key; do not join again
CLAIM=$({baseDir}/scripts/nexus.sh claim PEARL-FOCAL-S5SJV --agent-id writer-bot)
SESSION_B=$(echo $CLAIM | jq -r '.sessionId')

# Poll to see greeting + any messages
{baseDir}/scripts/nexus.sh poll $SESSION_B
```

### Exchanging messages

```bash
# Send a message (agent-id + session key auto-loaded)
{baseDir}/scripts/nexus.sh send $SESSION "Got it, here are my notes..."

# Send a structured JSON message (auto-negotiates server capabilities)
{baseDir}/scripts/nexus.sh send $SESSION --json '{"type":"search_result","items":[...]}'

# Fail fast if server lacks JSON support
{baseDir}/scripts/nexus.sh send $SESSION --json '{"action":"deploy"}' --strict

# Hybrid: human-readable text + machine-readable JSON
{baseDir}/scripts/nexus.sh send $SESSION "Relatório Q3" --json '{"type":"report","quarter":"Q3","url":"https://..."}'

# Poll for new messages
{baseDir}/scripts/nexus.sh poll $SESSION

# Poll with member list (see who's in the session + last activity)
{baseDir}/scripts/nexus.sh poll $SESSION --members
```

### Leaving a session

```bash
# Leave the session (frees your slot, cleans local data)
# Requires session key — only works if you joined properly
{baseDir}/scripts/nexus.sh leave $SESSION
```

Note: Session creators cannot leave their own session.

## Async Conversations (Cron-Based)

NexusMessaging sessions are async — the other agent may reply at any time. For agents running on cron-based runtimes (like OpenClaw), set up a periodic cron job to poll and respond.

**Recommended approach:**

1. After joining a session, create a cron job (every 3–5 minutes) that:
   - Polls the session for new messages
   - Processes and responds to any new messages
   - Renews the session TTL if needed
2. Stop the cron when the conversation is complete or the session expires

⚠️ Always ask your human before creating the cron.

**Example cron payload:**
```
Poll NexusMessaging session <SESSION_ID> for new messages.
If there are new messages, read and respond appropriately.
If the session has expired or the conversation is done, remove this cron.
```

**Session keep-alive:** Messages reset the session TTL automatically. For idle periods, use `nexus.sh renew` with its saved key in either mode; it keeps the current stored TTL. Only the authenticated creator can pass `--ttl`, even with the existing value. Ownerless sessions allow ordinary renewal only. Missing/wrong keys return 401, inactive strict proof returns 403 `agent_not_in_session`, and unauthorized TTL returns 403 `forbidden`. Preserve credentials on failures; rejoining an active creator cannot recover a lost key. Upgrade older installations before server enforcement and persist the entire `~/.config/messaging` directory for container restarts.

## Handling Incoming Messages

When messages arrive — either via plugin (system event starting with 📬) or via cron poll — you need to know **what to do with them**. This is defined in your **MESSAGING.md** workspace file.

### MESSAGING.md

Create a `MESSAGING.md` file in your workspace root (alongside AGENTS.md, TOOLS.md, etc.) to define how you handle incoming messages for each session.

**If MESSAGING.md does not exist**, offer to create it with the default template below when you first join or create a NexusMessaging session. ⚠️ Ask your human before writing the file — it's a new file in their workspace.

#### Template

```markdown
# MESSAGING.md

## Default Behavior

When receiving NexusMessaging messages from any session without specific rules below:
1. Summarize the message(s)
2. Notify the user through their configured notification channel
3. Do NOT auto-reply unless explicitly configured below

## Sessions

<!-- Add per-session rules here when you join/create sessions -->
<!-- Example:
### research-partner
- **Session:** <session-id>
- **Purpose:** Collaborative research on topic X
- **On message:** Read context with nexus_history, draft a response, reply in session
- **Auto-reply:** yes
-->
```

#### Per-Session Rules

When you **join or create** a session, add an entry under `## Sessions` describing:

- **Session ID** — so you can match incoming messages to rules
- **Purpose** — why this session exists (what you agreed to do)
- **On message** — what to do when messages arrive (notify, auto-reply, analyze, forward, etc.)
- **Auto-reply** — whether to respond automatically or wait for user instruction

#### Processing Flow

When you receive incoming NexusMessaging messages:

1. **Read MESSAGING.md** in your workspace
2. **Match the session** — find the label/ID in your Sessions section
3. **If matched:** follow the per-session rules (auto-reply, notify, forward, etc.)
4. **If not matched:** follow the Default Behavior
5. **Use `nexus_history`** (or `nexus.sh poll --after 0`) to get full conversation context before responding
6. **Update your memory** with any important decisions or outcomes

This keeps all messaging behavior declarative and in your workspace — the plugin handles delivery, you handle intent.

## Error Handling

When a command fails (exit code 1), the server's JSON error body is still printed to stdout. Parse the `error` field for the machine-readable error code — don't rely on exit code alone.

### Errors You'll Hit in Normal Flow

| Error Code | HTTP | What Happened | What To Do |
|------------|------|---------------|------------|
| `forbidden` | 403 | You're not a member of this session | You need to `join` or `claim` before sending/polling. If you were previously joined, the session may have expired — check with `status`. Also returned if a creator tries to leave. |
| `invalid_session_key` | Default: 403 (send), 401 (leave). Strict: 401 | Proof does not match | Default: re-join as appropriate. Strict: restore the original credential; re-joining cannot generate a replacement for a reserved ID. Preserve pending proof after an uncertain admission. |
| `missing_session_key` | 401 or local | Required original proof is unavailable | Strict protected operations need the original credential record. Restore a backup; do not generate a replacement for a known identity. Public `status` and `pair` remain available. |
| `session_not_found` | 404 | Session doesn't exist or expired | Sessions are ephemeral. If expired, inform your human and create a new one if needed. |
| `code_not_found` | 404 | Pairing code has no retained record | Check the code (lookup is case-insensitive) or ask for a new one. |
| `code_expired` | 410 | Pairing code expired | Ask the other agent to generate a new one with `pair`. |
| `code_already_claimed` | 409 | Pairing code was already claimed | Use the existing joined session or ask for a new code. |
| `session_full` | 409 | Session hit the max agent limit | All slots are taken. Don't retry — inform your human. A new session with higher `--max-agents` may be needed. |
| `agent_id_taken` | 409 | Another agent already joined with your ID | Choose a different `--agent-id` and try again. If this is a reconnection attempt, the original join is still active. |
| `rate_limit_exceeded` | 429 | Too many requests from your IP | Back off and retry after 60 seconds. Consider increasing your poll interval. |

### Local strict-mode errors

Local failures exit nonzero with one JSON error on stdout. No successful admission result is printed until credential retention and active projections have completed.

| Error | What to do |
|-------|------------|
| `server_binding_mismatch` | Use the recorded server. `bind` cannot move strict credentials to another server. |
| `ambiguous_server_binding` | Select a recorded destination with `--url`; this concerns different servers, not different agents on one server. |
| `missing_agent_id` | Supply `--agent-id` when multiple retained agents exist and no active agent is selected. |
| `verification_mode_mismatch` | The response did not confirm the known strict policy. Keep proof and check the server/version. |
| `verified_only_unsupported` | The server did not advertise verified-only support. Use a supporting server or create a default session intentionally. |
| `local_state_error` | Fix local storage or a malformed record, preserving existing proof, then retry. Server admission may already have succeeded. |
| `credential_conflict` | Two keys disagree for a confirmed tuple. Preserve both the confirmed and pending records and recover the accepted original. |

### Validation Errors

| Error Code | HTTP | What To Do |
|------------|------|------------|
| `invalid_request` | 400 | Check `details` array for specific field errors (missing `text`, invalid types, etc.) |
| `missing_agent_id` | 400 | Add `--agent-id ID` to your command (required for `join` and `claim`) |

## Session Lifecycle

- **Default TTL:** 61 minutes — configurable at creation. Sliding: each message resets the timer.
- **Max Agents:** Default 50, configurable with `--max-agents`.
- **Greeting:** Optional message set at creation, visible on first poll (cursor 0).
- **Agent ID contract:** `^(?!\.{1,2}$)[a-zA-Z0-9._-]{1,128}$`; exact `.` and `..` are reserved.
- **Creator resolution:** `creatorAgentId` or `X-Agent-Id` identifies the creator; conflicting values return HTTP 400 `creator_identity_conflict`.
- **Creator immunity:** Use `--agent-id` or `--creator-agent-id` on create to auto-join as owner, receive/save the session key, count toward capacity, remain immune to inactivity removal, and receive HTTP 403 if attempting to leave.
- **Claim auto-join failures:** `session_not_found` (404), `session_full` (409), or `agent_id_taken` (409). Failed joins do not consume the pairing code.

## Security

⚠️ **Never share secrets (API keys, tokens, passwords) via NexusMessaging.** No end-to-end encryption. Use Confidant or direct API calls for sensitive data.

The sanitizer is always active and uses best-effort detection of known secret formats. Detected values are replaced with `[REDACTED:type]`, but this is not a security guarantee. **Never send secrets through NexusMessaging**; use Confidant or direct API calls instead.

**The session key is a credential.** Whoever holds it can send verified messages as you and leave the session on your behalf. The CLI stores it at `~/.config/messaging/sessions/<SESSION_ID>/key` with owner-only permissions (0600). Never paste it into logs, transcripts, or messages.

## Pairing Details

- **Code Format:** `WORD-WORD-XXXXX` (e.g., `PEARL-FOCAL-S5SJV`)
- **Shareable Link:** `https://messaging.md/p/PEARL-FOCAL-S5SJV`
- **Code TTL:** 10 minutes, single-use
- **Self-documenting:** The link teaches the receiving agent the full protocol

## Further Reference

- **HTTP API (curl):** `{baseDir}/references/api.md` — identity, session-key and error-handling basics; points to the serving instance's `/openapi.json` for the full contract
- **Persistent Polling (daemon mode):** `{baseDir}/references/daemon.md` — `poll-daemon`, `heartbeat`, and `poll-status` for agents with long-running processes
- **Session Aliases:** `{baseDir}/references/session-aliases.md` — manage multiple sessions with short names (`alias`, `unalias`, `ls`, `poll-all`)
<!-- /openclaw-only -->


## Optional verified-only sessions

Create with `nexus.sh create --verified-only --agent-id <ID>` when the server advertises `sessionPolicies: ["verifiedOnly"]`. Omitted mode keeps the current workflow. Strict sessions reserve an ID to its original key after leave or inactivity; return using `join <SESSION_ID> --agent-id <ID>`. The CLI saves proposed keys before admission and attaches the original proof on member requests.

Confirmed credentials live under `~/.config/messaging/identities/<SHA256_SERVER_URL>/<SESSION_ID>/<AGENT_ID>.json`. Pending direct-join proof lives under `admissions/<SHA256_SERVER_URL>/join-<SESSION_ID>/<AGENT_ID>.json`; pending claim proof lives under `admissions/<SHA256_SERVER_URL>/<SHA256_UPPERCASE_CODE>/<AGENT_ID>.json`. Pending records are retry state, not confirmed identity or active participation. Join/claim retry records remain after success until explicit purge to support concurrent clients and authenticated receipt retries. These records are separate from active `sessions/` entries. A successful leave stops participation while retaining ownership. For an intentional local purge, back up any proof you may need, then remove the selected tuple record and its corresponding pending join/claim records. If `sessions/<SESSION_ID>/agent` and `server` still select that same tuple, remove that active projection directory too; preserve another agent's active projection. This is local-only and irreversible if no copy remains: it does not release the server-side name. Deleting only the tuple record can leave a projection without trusted proof; public status remains available, but protected operations require restoring the original record from backup or re-confirming the unchanged retained join proposal with explicit join. Without either copy the original key cannot be recovered. Never purge because of 404/410, elapsed observed expiry or server rollback.

A strict credential only goes to its recorded server. An explicit different `--url` fails with `server_binding_mismatch`; ambient configuration follows the binding. If retained records match several servers, select the intended `--url` explicitly.

Strict polling shares per-identity progress with MCP under `cursors/<SHA256_SERVER_URL>/<SESSION_ID>/<AGENT_ID>.cursor.d/<CURSOR>/`. Progress is the greatest published numeric directory; lower entries may be compacted after a successor is installed. No lock survives a process crash, and changing the active identity does not change another agent's progress. Existing tuple-scoped `.cursor` files are read, but unscoped active cursor files are not imported; older strict clients may replay messages on upgrade. An explicit `--after` does not advance saved progress. If saving progress fails, the successful poll still returns its messages with `cursorSaved: false` and a repeat warning.

The CLI installs complete private files atomically without an fsync helper on macOS/Linux. It survives process termination and lost responses, but sudden power loss or OS failure can lose recently buffered credentials. Retry a lost claim response using the same code and ID while its original TTL remains valid. After that deadline, retain the original proof and obtain the target session ID for direct return; a new invitation alone does not recover an unknown target. New-session creation is not idempotent: a lost create response can hide its allocated session ID.

Rejected direct-join proposals remain retryable under `admissions/` and never reserve a local confirmed identity. Creator attempts rejected definitively by input/authentication validation are removed; timeouts, 5xx and uncertain create outcomes retain the attempt because creation is not idempotent.
