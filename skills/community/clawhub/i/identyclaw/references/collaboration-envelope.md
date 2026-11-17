# Channel-Agnostic Collaboration Envelope

**Schema:** `identyclaw.collaboration.v1`  
**MCP resource URI:** `doc:reference:collaboration-envelope`

IdentyClaw provides **identity and trust**, not transport. Email, chat, webhooks, game private side-channels, and paste-in-message channels each need a shared envelope so agents can attach cryptographic trust (HOLA), carry a task payload, and verify inbound messages uniformly.

**HOLA travels offline, peer-to-peer.** Agents exchange envelopes and HOLA lines **directly** on the channel they already use. Each peer **verifies independently** (IdentyClaw API or direct NEAR RPC — peer's choice). Do not route HOLA **exchange** through IdentyClaw HTTP API or a game server — those are separate services, not brokers for the wire path.

**Related:** MCP `doc:reference:inter-agent-communication` (optional email/Himalaya patterns — **out of scope** for the ClawHub `identyclaw` skill; A2A uses the separate plugin), [`multi-tenant-collaboration.md`](multi-tenant-collaboration.md) (operator patterns), [`identity-verification-policy.md`](identity-verification-policy.md) (proof bar), `doc:reference:hola-subagent-authentication`, `doc:reference:openclaw-integration-guide`.

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

**Verify before execute** — the norm for every channel. Copy-paste verifier recipes: [`verify-hola-recipes.md`](verify-hola-recipes.md) (MCP `doc:reference:verify-hola-recipes`).

1. **Parse** — valid JSON, `schema === identyclaw.collaboration.v1`, required fields present.
2. **Freshness** — `timestamp` within acceptable window (align with HOLA nonce TTL, ~5 minutes).
3. **Trust HOLA** — each receiving peer verifies **independently**: **IdentyClaw API** (`POST /api/identity/verify`) or **direct NEAR RPC** (e.g. `@rodit/rodit-auth-be`) — peer's choice. Proceed only when the full proof bar passes.
4. **Identity match** — `result.peerTokenId` must equal `from.tokenId` (impersonation guard).
5. **Subagent** — if delegation fields present in HOLA, `POST /api/isauthorizedsigner` must return `authorized: true`.
6. **Lookup** — optional `GET /api/identity/token/{peerTokenId}/full` for `contactUri` and traits (self-declared).
7. **Process task** — execute `task.payload` only after steps 3–5 pass.

```bash
curl -sS -X POST https://api.identyclaw.com/api/identity/verify \
  -H "Content-Type: application/json" \
  -d '{"hola":"<envelope.hola>"}'
# Optional: -H "Authorization: Bearer $JWT"
```

Trust **full independent validation** (either verify path) — not local checksum checks alone.

---

## Embedding rules by channel

### Email

- **Subject:** `{channelHints.subjectPrefix}{task.type}` — e.g. `TASK_REQUEST:benchmark`
- **Body:** JSON envelope in a fenced code block, or `Content-Type: application/json` attachment named `identyclaw-envelope.json`
- **HOLA alternative:** Include `hola` in body text per MCP `doc:reference:inter-agent-communication` (email channel) or verify over A2A with the separate plugin

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

### Hermes / IronClaw / NanoClaw / generic HTTP agent

1. Agent receives envelope JSON on Telegram, Discord, email, HTTP, or paste.
2. `POST /api/identity/verify` with `envelope.hola` (public — no JWT).
3. On `verified: true`, match `peerTokenId` to `from.tokenId`.
4. Execute `task.payload` only after steps 2–3 succeed.
5. Reply with a new envelope + fresh HOLA on the same channel.

Login for outbound HOLA: host script [`scripts/identyclaw-login.mjs`](../../scripts/identyclaw-login.mjs) or `@rodit/hola-client`. See [`agent-frameworks.md`](agent-frameworks.md#what-this-api--repo-provides-all-runtimes).

### Non-OpenClaw webhook ingress

Same crypto as the OpenClaw webhooks plugin; different host:

1. Set Passport `webhook_url` to your agent HTTPS **base** (no required `/hooks/agent` in metadata).
2. Trusted host process listens on `/webhook`, `/hooks/agent`, or your path.
3. Verify Ed25519 with `@rodit/rodit-auth-be` — reject invalid signatures.
4. If payload includes `hola` or a collaboration envelope, run verify-before-execute (order above) before tools.

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
- Programmatic builders live in `@rodit/hola-client` (`buildCollaborationEnvelope`, `parseCollaborationEnvelope`, `formatSessionsSendMessage`). Reference skill: `identyclaw-a2a-trust-skill/` (covers `sessions_send` and A2A message bodies; A2A wire auth is `@identyclaw/openclaw-a2a-plugin` P2P JWT only).

---

## OpenClaw plugin tools

| Tool | Use |
| --- | --- |
| `identyclaw_verify_hola` | Step 3 — trust decision |
| `identyclaw_get_agent_identity` | Step 6 — `contactUri` and DN |
| `identyclaw_check_subagent_signer` | Step 5 — delegation |

Install: `openclaw plugins install clawhub:@identyclaw/openclaw-identyclaw-plugin`
