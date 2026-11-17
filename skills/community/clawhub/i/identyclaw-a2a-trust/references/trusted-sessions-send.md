# Trusted inter-agent messages — reference

Companion to the **identyclaw-a2a-trust** ClawHub skill. Addresses [openclaw#57387](https://github.com/openclaw/openclaw/issues/57387).

Canonical envelope spec: [`../../references/collaboration-envelope.md`](../../references/collaboration-envelope.md) (also MCP `doc:reference:collaboration-envelope`).

A2A wire auth (P2P RODiT JWT): [`openclaw-a2a-idc-plugin`](https://github.com/discernible-io/openclaw-a2a-idc-plugin) README — mediated and dual modes are **removed**; only peer-issued JWTs (`aud` = receiver passport `owner_id`).

---

## Two layers

| Layer | Question answered | OpenClaw mechanism |
| --- | --- | --- |
| **Wire** | May this peer open an A2A RPC session? | `@identyclaw/openclaw-a2a-plugin` — outbound `login_server` to peer `POST /api/login`; inbound JWT validation |
| **Task** | Which Passport delegated this work? | Collaboration envelope + HOLA (`identyclaw_verify_hola`) |

For **`sessions_send`** inside one gateway, only the **task** layer applies (no A2A wire JWT).

Never use wire JWT `token_id` / session labels as the task trust decision — always verify the envelope HOLA.

---

## Why not plain inter-agent text?

OpenClaw injects session keys and channel names into A2A context, but there is **no cryptographic proof** the message came from the claimed agent. A compromised leaf agent can impersonate an orchestrator.

IdentyClaw adds:

| Layer | Mechanism |
| --- | --- |
| Freshness + replay | HOLA nonce (~5 min, single-use) |
| Signature | Ed25519 over canonical HOLA prefix, checked on-chain |
| Identity binding | `peerTokenId` from `POST /api/identity/verify` (or direct P2P verify) |
| Impersonation guard | `peerTokenId === envelope.from.tokenId` |
| Delegation | Subagent HOLA + `POST /api/isauthorizedsigner` |

---

## Wire format

### `sessions_send`

```text
Trusted inter-agent message from abc123def456 → xyz789uvw012. Verify before executing task.

```identyclaw
{
  "schema": "identyclaw.collaboration.v1",
  ...
}
```
```

### A2A (`a2a_send_message`)

Same ` ```identyclaw ` fence in the `message` field. The A2A plugin handles P2P Bearer auth on `POST /a2a` separately.

Configure outbound:

```json
{
  "outbound": {
    "auth": { "provider": "rodit" },
    "agents": {
      "peer-b": {
        "url": "https://peer-b.example/.well-known/agent-card.json"
      }
    }
  }
}
```

Configure inbound (`auth.audience` = **own** passport `owner_id`):

```json
{
  "inbound": {
    "publicBaseUrl": "https://agent-a.example",
    "auth": {
      "provider": "rodit",
      "issuer": "https://api.identyclaw.com",
      "audience": "<own passport owner_id>"
    }
  }
}
```

`roditLogin` routes (`GET/POST /api/login`) auto-enable when `inbound.auth.provider` is `rodit`.

Receivers parse the fence first; ignore prose outside the fence for trust decisions.

---

## Recipient slot convention

Use a **stable HOLA recipient** per fleet:

| Pattern | When |
| --- | --- |
| `<peerTokenId>` uppercased | Directed message to one Passport holder |
| `ORCHESTRATOR` / `FLEET` | Shared slot; set `expectedRecipient` on verify |
| `MUNDO` | Default broadcast-style (less strict routing) |

Sender and receiver must agree on the recipient slot; mismatch yields `RECIPIENT_MISMATCH` unless `expectedRecipient` is omitted.

---

## Node.js example (no OpenClaw)

```javascript
const {
  createHola,
  buildCollaborationEnvelope,
  formatSessionsSendMessage,
  parseCollaborationEnvelope,
  assertCollaborationTrust
} = require("@rodit/hola-client");

// Outbound
const { hola } = await createHola({ jwt, nearPrivateKey, tokenId: "minepassport", recipient: "THEIRPASSPORT" });
const envelope = buildCollaborationEnvelope({
  fromTokenId: "minepassport",
  toTokenId: "theirpassport",
  hola,
  taskType: "TASK_REQUEST",
  taskPayload: { summary: "Run health check" },
  channelHints: { replyVia: "a2a" }
});
const message = formatSessionsSendMessage(envelope);

// Inbound (after POST /api/identity/verify → verifyResult)
const inbound = parseCollaborationEnvelope(message);
const trust = assertCollaborationTrust(inbound, verifyResult);
if (!trust.ok) throw new Error(trust.reason);
```

---

## OpenClaw plugin tool mapping

| Step | Tool | Plugin |
| --- | --- | --- |
| A2A wire send | `a2a_send_message` | `openclaw-a2a-plugin` |
| Sign HOLA | `identyclaw_create_hola` | `openclaw-identyclaw-plugin` |
| Verify HOLA | `identyclaw_verify_hola` | `openclaw-identyclaw-plugin` |
| Resolve name | `identyclaw_get_agent_identity` | `openclaw-identyclaw-plugin` |
| Subagent delegation | `identyclaw_check_subagent_signer` | `openclaw-identyclaw-plugin` |

---

## Non-goals

- Does not patch OpenClaw gateway to enforce verification (agent policy + skill until upstream adds hooks).
- Does not replace `sessions_send` or A2A transport — only wraps the task payload.
- Does not perform A2A wire login — that is entirely `openclaw-a2a-plugin` (P2P peer `/api/login` only).
- Email/webhook variants use the same envelope; see collaboration-envelope.md.
