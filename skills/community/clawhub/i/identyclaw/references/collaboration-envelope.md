# Channel-Agnostic Collaboration Envelope

**Schema:** `identyclaw.collaboration.v1`  
**MCP resource URI:** `doc:reference:collaboration-envelope`

IdentyClaw provides **identity and trust**, not transport. Email, chat, webhooks, and paste-in-message channels each need a shared envelope so agents can attach cryptographic trust (HOLA), carry a task payload, and verify inbound messages uniformly.

**Related:** [`inter-agent-communication.md`](inter-agent-communication.md) (email/Himalaya patterns), `doc:reference:hola-subagent-authentication`, `doc:reference:openclaw-integration-guide`.

---

## Envelope shape

```json
{
  "schema": "identyclaw.collaboration.v1",
  "messageId": "01HXABCDEFGHJKMNPQRSTVWXYZ0",
  "timestamp": "2026-06-06T12:00:00.000Z",
  "from": { "tokenId": "bkbvehbdcrgm" },
  "to": { "tokenId": "lncnsfsnskzr", "contactUri": "mailto:agent@example.com" },
  "hola": "HOLA/MUNDO/bkbvehbdcrgm/2026-06-06T12:00:00.000Z/4F9A3C7E2D1B9A4C/API.IDENTYCLAW.COM/MFRGG.../J",
  "task": {
    "type": "TASK_REQUEST",
    "payload": {
      "summary": "Run benchmark X and return JSON metrics"
    }
  },
  "channelHints": {
    "replyVia": "contactUri",
    "subjectPrefix": "TASK_RESULT:"
  }
}
```

| Field | Required | Notes |
| --- | --- | --- |
| `schema` | yes | Must be `identyclaw.collaboration.v1` |
| `messageId` | yes | ULID or UUID — dedupe on receiver |
| `timestamp` | yes | ISO 8601 UTC — reject stale envelopes beyond HOLA TTL |
| `from.tokenId` | yes | Sender Passport ID (12 lowercase letters) |
| `to.tokenId` | no | Intended recipient Passport ID |
| `to.contactUri` | no | Routing hint from sender's view (`mailto:`, `https://`, etc.) |
| `hola` | yes* | Full HOLA line from sender (*omit only in trusted internal channels with separate verify) |
| `task` | yes | `{ type, payload }` — channel-independent work description |
| `channelHints` | no | Reply routing (`subjectPrefix`, `replyVia`) |

**Subagent delegation:** When `hola` uses the subagent format, also run `POST /api/isauthorizedsigner` after verify succeeds — see `doc:reference:hola-subagent-authentication`.

---

## Verification order (receiver)

1. **Parse** — valid JSON, `schema === identyclaw.collaboration.v1`, required fields present.
2. **Freshness** — `timestamp` within acceptable window (align with HOLA nonce TTL, ~5 minutes).
3. **Trust HOLA** — `POST /api/identity/verify` with `{ "hola": "<envelope.hola>" }`. Proceed only when `verified: true`.
4. **Identity match** — `result.peerTokenId` must equal `from.tokenId` (impersonation guard).
5. **Subagent** — if delegation fields present in HOLA, `POST /api/isauthorizedsigner` must return `authorized: true`.
6. **Lookup** — optional `GET /api/identity/token/{peerTokenId}/full` for `contactUri` and traits (self-declared).
7. **Process task** — execute `task.payload` only after steps 3–5 pass.

```bash
curl -sS -X POST https://api.identyclaw.com/api/identity/verify \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"hola":"<envelope.hola>"}'
```

Trust **`verified: true`** from the API — not local checksum checks alone.

---

## Embedding rules by channel

### Email

- **Subject:** `{channelHints.subjectPrefix}{task.type}` — e.g. `TASK_REQUEST:benchmark`
- **Body:** JSON envelope in a fenced code block, or `Content-Type: application/json` attachment named `identyclaw-envelope.json`
- **HOLA alternative:** Include `hola` in body text per [`inter-agent-communication.md`](inter-agent-communication.md)

Example subject/body:

```text
Subject: TASK_REQUEST:benchmark
Body:
--- identyclaw.collaboration.v1 ---
{ ... full JSON envelope ... }
```

### OpenClaw webhook (`/hooks/agent`)

- POST body may wrap the envelope in `data.envelope` or pass the envelope as the root JSON when the event originates from a trusted bridge.
- Map `task.type` to an isolated agent prompt; verify `hola` before tool execution — see `doc:reference:openclaw-integration-guide`.

### Chat / paste block

```text
```identyclaw
{ ... envelope JSON ... }
```
```

Receivers extract the block, then run the verification order above.

---

## Example flows

### Email outbound (agent A → agent B)

1. A fetches nonce, signs HOLA to B's recipient slot.
2. A builds envelope with `task.type: "TASK_REQUEST"`.
3. A sends via Himalaya/SMTP to B's `contactUri` (`mailto:...`).
4. B parses envelope → verify HOLA → processes task → replies with `TASK_RESULT:` envelope.

### OpenClaw inbound webhook

1. IdentyClaw or a bridge POSTs to `/hooks/agent` with envelope in body.
2. OpenClaw agent verifies webhook signature (IdentyClaw-origin events) separately from HOLA trust.
3. Agent calls `identyclaw_verify_hola` / `/api/identity/verify` on `envelope.hola`.
4. On success, spawn task from `envelope.task.payload`.

---

## Replay and stale messages

- HOLA nonces are single-use (~5 minute window) — stale `timestamp` or replayed nonce → `verified: false`.
- Receivers should dedupe on `messageId`.
- Reject envelopes whose `timestamp` is far in the future or past relative to receiver clock.

---

## Non-goals

- IdentyClaw does **not** deliver messages — transport remains Himalaya, webhooks, human paste, etc.
- This spec does **not** change the HOLA wire format — it wraps existing lines.
- Programmatic builders live in `@rodit/hola-client` (`buildCollaborationEnvelope`, `parseCollaborationEnvelope`, `formatSessionsSendMessage`). Reference skill: `identyclaw-a2a-trust-skill/`.

---

## OpenClaw plugin tools

| Tool | Use |
| --- | --- |
| `identyclaw_verify_hola` | Step 3 — trust decision |
| `identyclaw_get_agent_identity` | Step 6 — `contactUri` and DN |
| `identyclaw_check_subagent_signer` | Step 5 — delegation |

Install: `openclaw plugins install clawhub:@identyclaw/openclaw-identyclaw-plugin`
