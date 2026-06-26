# kemia API v1 — Reference

Base URL: `https://kemia.byte5.ai` (or your self-hosted instance)

## Authentication

### Enrollment (initial setup)

The enrollment flow creates a new kemia instance and returns an API key. No shared secrets required.

```
POST /api/v1/enroll              → { enrollUrl, pollUrl }  (no auth)
GET  /api/v1/enroll/:code/status → { status, apiKey? }     (no auth, code is auth)
POST /api/v1/enroll/:code/ack    → { status: "acked" }     (no auth, code is auth)
```

### Bearer Token (all other endpoints)

After enrollment, all API calls use the API key as a Bearer token:

```
Authorization: Bearer km_abc123...
```

The API key is returned once during enrollment polling and never stored in plaintext on the server.

---

## Enrollment Flow

### Step 1: Start enrollment

```
POST /api/v1/enroll
```

**Auth:** None (rate-limited: 5/min per IP)

**Request:**
```json
{
  "name": "My Instance",
  "orchestrator": "openclaw",
  "fingerprint": "sha256:abc123..."
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | "My Instance" | Display name for the kemia instance |
| `orchestrator` | string | "openclaw" | Orchestrator type: `"openclaw"`, `"paperclip"`, or custom |
| `fingerprint` | string | *(none)* | Optional stable ID for this machine (e.g. `sha256(hostname + workspace_path)`). If it matches an existing instance, the confirm page offers Re-Auth instead of silently creating a duplicate. Max 200 chars. |

**Response (200):**
```json
{
  "enrollUrl": "https://kemia.byte5.ai/enroll/km_enr_abc123...",
  "pollUrl": "/api/v1/enroll/km_enr_abc123.../status",
  "expiresAt": "2026-03-28T12:15:00.000Z"
}
```

The orchestrator shows `enrollUrl` to the human operator. The code is in the URL — no manual entry needed. Expires in 15 minutes, single-use.

### Step 2: Human confirms

The human clicks `enrollUrl` → lands on a confirmation page → clicks "Connect" → instance + session created → redirected to dashboard.

### Step 3: Poll for API key

```
GET /api/v1/enroll/:code/status
```

**Auth:** None (the code IS the auth; rate-limited: 30/min per IP)

**Response (pending):**
```json
{ "status": "pending" }
```

**Response (completed — API key returned within the retention window):**
```json
{
  "status": "completed",
  "instanceId": "clxyz...",
  "apiKey": "km_abc123..."
}
```

The API key is retrievable for a short retention window (5 minutes) after
confirmation. Within that window, repeated polls return the same key — this
lets a client that crashes mid-save recover without re-enrolling. After the
window elapses, the next poll clears the stored key and returns without it:

```json
{ "status": "completed", "instanceId": "clxyz..." }
```

Clients that have persisted the key should call `POST .../ack` to clear it
server-side immediately, rather than waiting out the window.

**Response (expired):**
```json
{ "status": "expired" }
```

### Step 4 (optional): Ack the stored key

```
POST /api/v1/enroll/:code/ack
```

**Auth:** None (the code IS the auth; rate-limited: 30/min per IP)

Signals that the client has persisted the API key and the server may clear
its stored (encrypted) copy now. Idempotent.

**Response (200):**
```json
{ "status": "acked" }
```

**Response (409):** Enrollment not yet completed.

---

## Endpoints

### `GET /api/v1/status`

Health check. Verifies API key is valid and returns instance identity.

**Auth:** Bearer token

**Response (200):**
```json
{
  "ok": true,
  "instanceId": "clxyz...",
  "instanceName": "my-instance"
}
```

---

### `POST /api/v1/agents`

Export/push agent configuration to kemia. Upserts the agent and fully replaces its config files.

**Auth:** Bearer token

**Request:**
```json
{
  "name": "CyberClaw",
  "description": "Main agent",
  "files": [
    { "filename": "SOUL.md", "content": "# Soul\n..." },
    { "filename": "IDENTITY.md", "content": "..." }
  ]
}
```

**Validation:**
- `name`: 1–100 chars, alphanumeric + hyphens/underscores (`^[a-zA-Z0-9_-]+$`)
- `files[].filename`: must match `^[A-Z][A-Z0-9_]*\.md$` (e.g. `SOUL.md`)
- `files[].content`: max 500KB per file
- `files`: 1–20 files per agent

**Response (200):**
```json
{
  "agentId": "clxyz...",
  "name": "CyberClaw"
}
```

---

### `GET /api/v1/agents/:agentId`

Get agent details and current config files.

**Auth:** Bearer token

**Response (200):**
```json
{
  "agent": {
    "id": "clxyz...",
    "name": "CyberClaw",
    "description": "Main agent",
    "createdAt": "2026-03-10T...",
    "updatedAt": "2026-03-10T..."
  },
  "files": [
    {
      "id": "clfile...",
      "filename": "SOUL.md",
      "content": "...",
      "updatedAt": "2026-03-10T..."
    }
  ]
}
```

---

### `GET /api/v1/agents/:agentId/profile`

Compact agent profile for external consumers (Paperclip plugin, dashboards, etc.).

**Auth:** Bearer token

**Response (200):**
```json
{
  "id": "clxyz...",
  "name": "CyberClaw",
  "description": "Main agent",
  "healthScore": 95,
  "healthLevel": "healthy",
  "persona": {
    "formality": 30,
    "directness": 70,
    "warmth": 80,
    "humor": 60,
    "sarcasm": 10,
    "conciseness": 50,
    "proactivity": 70,
    "autonomy": 60,
    "riskTolerance": 40,
    "creativity": 65,
    "drama": 30,
    "philosophy": 45
  },
  "role": {
    "jobTitle": "Customer Support",
    "taskCount": 4,
    "boundaryCount": 3,
    "ruleCount": 5
  },
  "knowledge": {
    "sourceCount": 2,
    "capabilityCount": 5
  },
  "team": {
    "humanInterface": true,
    "escalationTarget": "Team Lead"
  },
  "fileCount": 3,
  "starterCount": 4,
  "updatedAt": "2026-03-28T..."
}
```

---

### `GET /api/v1/agents/:agentId/deploy`

Fetch the deploy-ready snapshot for an agent. This is what orchestrators poll to import edited configs.

**Auth:** Bearer token

**Response (200):**
```json
{
  "snapshot": {
    "id": "clsnap...",
    "name": "v2-tweaks",
    "description": "Adjusted personality",
    "createdAt": "2026-03-10T..."
  },
  "files": [
    { "filename": "SOUL.md", "content": "..." },
    { "filename": "IDENTITY.md", "content": "..." }
  ]
}
```

**Response (404):** No deploy-ready snapshot exists.

---

### `GET /api/v1/agents/:agentId/health`

Agent Guardian health check — config drift detection.

**Auth:** Bearer token

**Response (200):**
```json
{
  "health": {
    "score": 85,
    "level": "warning",
    "files": [
      { "filename": "SOUL.md", "status": "aligned" },
      { "filename": "AGENTS.md", "status": "drifted" }
    ],
    "suggestions": ["AGENTS.md has changed since last deploy"],
    "hasDeployBaseline": true
  }
}
```

---

### `POST /api/v1/auth-token`

Generate a one-time login URL for the web interface. Use this when the user needs a new session (e.g. expired, different device).

**Auth:** Bearer token

**Response (200):**
```json
{
  "token": "raw-token-value",
  "url": "https://kemia.byte5.ai/auth/token?t=raw-token-value",
  "expiresAt": "2026-03-10T12:15:00.000Z",
  "message": "Send this URL to the user. It expires in 15 minutes and can only be used once."
}
```

---

### `POST /api/v1/connect` (DEPRECATED)

**Status: 410 Gone.** Use `POST /api/v1/enroll` instead.

---

## Error Responses

All errors follow this format:
```json
{ "error": "Human-readable error message" }
```

| Status | Meaning |
|--------|---------|
| 400 | Validation error (bad input) |
| 401 | Missing/invalid API key |
| 404 | Resource not found |
| 409 | Conflict (e.g. enrollment already used) |
| 410 | Gone (deprecated endpoint) |
| 429 | Rate limited — check `Retry-After` header |
| 500 | Server error |

---

## Integration Guide

### For OpenClaw Skills

```bash
# 1. Start enrollment
RESPONSE=$(curl -sf -X POST -H "Content-Type: application/json" \
  -d '{"name":"My Agent","orchestrator":"openclaw"}' \
  https://kemia.byte5.ai/api/v1/enroll)

# 2. Show URL to user
echo "$RESPONSE" | jq -r '.enrollUrl'

# 3. Poll until confirmed
while true; do
  STATUS=$(curl -sf "https://kemia.byte5.ai$(echo $RESPONSE | jq -r '.pollUrl')")
  [ "$(echo $STATUS | jq -r '.status')" = "completed" ] && break
  sleep 10
done

# 4. Save API key
echo "$STATUS" | jq -r '.apiKey'
```

### For Paperclip Plugins

```typescript
// 1. Start enrollment
const { enrollUrl, pollUrl } = await ctx.http
  .fetch(`${kemiaUrl}/api/v1/enroll`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: "Paperclip", orchestrator: "paperclip" }),
  })
  .then((r) => r.json());

// 2. Show enrollUrl to user (in Board UI)

// 3. Poll for completion
const { status, apiKey } = await ctx.http
  .fetch(`${kemiaUrl}${pollUrl}`)
  .then((r) => r.json());

// 4. Store apiKey in plugin state
```

---

## Data Model

```
Instance (tenant)
  ├── Agent[]
  │     ├── ConfigFile[]         (current working state)
  │     ├── Snapshot[]           (versioned checkpoints)
  │     │     └── SnapshotFile[]
  │     ├── KnowledgeSource[]    (domain knowledge)
  │     ├── Capability[]         (tool toggles)
  │     └── ConversationStarter[]
  ├── Team[]
  │     └── TeamEdge[]           (agent relationships)
  ├── Deployment[]               (cross-instance pushes)
  ├── AuthToken[]                (one-time login links)
  └── Enrollment[]               (pending/completed enrollments)
```

- One Instance = one orchestrator deployment (OpenClaw, Paperclip, etc.)
- An Instance can have multiple Agents
- Each Agent has ConfigFiles (live state) and Snapshots (versions)
- A Snapshot can be marked `deployReady` for import by the orchestrator
