# OpenClaw Integration Guide

Wire IdentyClaw Passport metadata and webhooks to an OpenClaw gateway so inbound identity events (HOLA validation outcomes, future attestation) trigger agent tasks.

**MCP resource URI:** `doc:reference:openclaw-integration-guide`

**Related:** `doc:discovery`, `doc:reference:collaboration-envelope`, [`login-authentication.md`](login-authentication.md) (webhook signature verification), [`token-metadata.md`](token-metadata.md) (`webhook_url` field).

---

## Install complementary artifacts

```text
Skill (workflows):     openclaw skills install clawhub:identyclaw
Plugin (tools):        openclaw plugins install clawhub:@identyclaw/openclaw-identyclaw-plugin
MCP (docs):            https://api.identyclaw.com/mcp
Discovery index:       doc:discovery
Cheat sheet:           doc:skills
```

The **plugin** covers outbound API calls (verify HOLA, list agents, fetch identity). This guide covers **inbound** events from IdentyClaw to your gateway.

---

## Passport metadata — base URL vs hook path

Set `webhook_url` in Passport metadata to the **OpenClaw gateway base** (no hook path):

```text
Passport metadata webhook_url:  https://my-openclaw.example.com
IdentyClaw POST target:         https://my-openclaw.example.com/hooks/agent
```

IdentyClaw appends hook paths when sending (`sendWebhookToEndpoint` in the API). Do **not** embed `/hooks/agent` in metadata unless your deployment expects a full URL without path appending.

Example metadata fragment:

```json
{
  "webhook_url": "https://my-openclaw.example.com",
  "webhook_cidr": "203.0.113.0/24"
}
```

Optional `webhook_cidr` restricts accepted source IPs when your gateway has a stable egress range.

---

## When to use `/hooks/agent` vs `/hooks/wake`

| Hook | OpenClaw behavior | IdentyClaw use case |
| --- | --- | --- |
| `/hooks/wake` | Enqueue heartbeat / system event for main session | Liveness nudge after validation |
| `/hooks/agent` | Run isolated agent task; optional reply to messaging channels | **Primary** — process HOLA verify outcomes, run follow-up logic |

**Recommendation:** Use **`/hooks/agent`** as the default integration point for identity-driven automation. Use `/hooks/wake` only when you need session keep-alive without a full task.

During development, successful `POST /api/testhola` validation fires webhooks to **both** paths when `WEBHOOK_TEST_ENABLED=true`.

---

## Event payload and task mapping

**Event type (development test):** `testhola_validation_success`

**Example payload** (from `/api/testhola` webhook delivery):

```json
{
  "event": "testhola_validation_success",
  "data": {
    "peerTokenId": "abc123def456",
    "serverTokenId": "xyz789uvw012",
    "recipient": "MUNDO",
    "timestamp": "2026-04-24T18:30:00.000Z",
    "endpoint": "/api/testhola"
  }
}
```

**OpenClaw task mapping (suggested prompt chain):**

1. Parse `event` and `data.peerTokenId`.
2. Call `identyclaw_verify_hola` or `POST /api/identity/verify` if the inbound message carries a HOLA line (webhook alone does not replace verify for untrusted channels).
3. Call `identyclaw_get_agent_identity` or `GET /api/identity/token/{tokenId}/full` for DN and `contactUri`.
4. Run delegated work; reply on the channel implied by `contactUri` or your collaboration envelope — see `doc:reference:collaboration-envelope`.

For inbound messages that embed a [collaboration envelope](collaboration-envelope.md), verify the envelope's `hola` field before processing `task`.

---

## Development vs production

| Setting | **development** | **main** |
| --- | --- | --- |
| `WEBHOOK_TEST_ENABLED` | `"true"` — testhola fires webhooks | `"false"` |
| `WEBHOOK_TLS_SKIP_VERIFY` | may be `"true"` (dev only) | must be `"false"` |
| Webhook signature verification | document `verifyWebhookSignature()` / `getWebhookHandler()` | **required** on receiver |

Test with `POST /api/testhola` in development before promoting Passport metadata on main.

---

## Receiver checklist (OpenClaw side)

1. Register Passport `webhook_url` pointing at your OpenClaw gateway host (base URL only).
2. Expose `/hooks/agent` (and optionally `/hooks/wake`) with TLS.
3. Verify Ed25519 webhook signatures per [`login-authentication.md`](login-authentication.md) — reject unsigned or invalid payloads.
4. Restrict source IPs with `webhook_cidr` when possible.
5. Install the IdentyClaw plugin and skill for outbound verify/lookup tools.
6. Map inbound payloads to agent prompts; never trust raw `peerTokenId` without verify when the channel is untrusted.

---

## End-to-end test flow

```bash
# 1. Set webhook_url on your Passport metadata (gateway base URL)
# 2. In development, ensure WEBHOOK_TEST_ENABLED=true on the API host
# 3. Login and self-test HOLA
JWT=...  # from POST /api/login
curl -sS -X POST https://api.identyclaw.com/api/testhola \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"hola":"<your valid HOLA line>"}'
# 4. Confirm OpenClaw received POST on /hooks/agent (and optionally /hooks/wake)
```

---

## Non-goals

- IdentyClaw does not host your OpenClaw gateway or deliver arbitrary chat messages.
- MCP (`https://api.identyclaw.com/mcp`) is docs-only — webhooks are HTTP POST to your gateway, not MCP resources.
- Outbound HOLA creation: `identyclaw_create_hola` (plugin) or `@rodit/hola-client`.
