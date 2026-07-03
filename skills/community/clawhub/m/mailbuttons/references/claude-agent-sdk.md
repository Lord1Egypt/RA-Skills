# Wiring Mailbuttons into a Claude Agent SDK app

This is the idiom reference for the **Claude Agent SDK (TypeScript)** target. It
covers how to connect an agent to a Mailbuttons **sandbox** inbox, the governed
send pattern, reading the key from the environment, and the inbound handler
shape. For tone/structure see the reference repo
`github.com/mailbuttons/claude-scheduling-agent-ts`.

Everything here is **sandbox-only**. None of it enables external send, promotes
to production, or widens a token's scope — those are human actions taken in the
dashboard or via `mailbuttons promote`.

## 1. The key comes from the environment, always

```ts
const API_URL = process.env.MAILBUTTONS_API_URL ?? "http://localhost:8000";
const API_KEY = process.env.MAILBUTTONS_API_KEY; // mb_sandbox_...
if (!API_KEY) throw new Error("Set MAILBUTTONS_API_KEY (a scoped sandbox token).");
```

Never inline the token into source, a tool definition, or a prompt. The scaffold
tool generates code that follows this rule; keep it that way.

## 2. The two MCP surfaces

There are two ways the agent reaches Mailbuttons. Pick one and stay consistent:

- **MCP server (recommended in-agent):** point the SDK at the Mailbuttons MCP
  server so the model calls `mailbuttons_*` tools directly. The server is
  launched over stdio:

  ```ts
  import { query } from "@anthropic-ai/claude-agent-sdk";

  const result = query({
    prompt: userTurn,
    options: {
      mcpServers: {
        mailbuttons: {
          command: "npx",
          args: ["-y", "@mailbuttons/mcp-server"],
          // The token is inherited from the parent env — not passed inline.
          env: { MAILBUTTONS_API_KEY: process.env.MAILBUTTONS_API_KEY! },
        },
      },
      // Let the agent read and send, but route sends through the governed tool.
      allowedTools: [
        "mcp__mailbuttons__mailbuttons_list_messages",
        "mcp__mailbuttons__mailbuttons_get_message",
        "mcp__mailbuttons__mailbuttons_get_thread",
        "mcp__mailbuttons__mailbuttons_send_email",
      ],
    },
  });
  ```

- **Direct REST wrapper (for your own glue code):** call `/api/v1/mcp/*` with
  `fetch`, as the scaffolded `send.ts` / `inbox.ts` do. Use this for the webhook
  receiver and any non-model code path.

## 3. The governed send pattern

A send never "just sends." The backend returns a governed outcome you must
handle. `blocked` and `draft_pending_approval` are **normal results, not
errors** — do not retry to force delivery, and do not treat them as failures.

| status | meaning | what to do |
|---|---|---|
| `sent` / `queued` | delivered (internal recipient) | done |
| `blocked` | recipient fails policy; `policy.matched_rule` says which | surface the rule; don't retry |
| `draft_pending_approval` | external recipient, token lacks `send_external` | tell the user a human must approve; parked as a draft |

```ts
const r = await governedSend({ to: ["teammate@sandbox.mailbuttons.app"], subject, text });
if (r.status === "blocked") {
  // Policy gate did its job. Show r.policy.matched_rule to the user.
} else if (r.status === "draft_pending_approval") {
  // External send is a human decision. Offer mailbuttons_request_promotion.
}
```

If the agent (or a malicious inbound message) tries to email an outside address,
this is exactly the wall it hits. That is the product working as designed.

## 4. Inbound handler shape

Inbound is a webhook (`email.received`) carrying metadata only. Verify the
`X-Mailbuttons-Signature` HMAC, then fetch the full message through the governed
read endpoint:

```ts
app.post("/webhook/mailbuttons", async (req, res) => {
  if (!verifySignature(req.rawBody, req.header("X-Mailbuttons-Signature"))) {
    return res.status(401).end();
  }
  await onInboundEmail({ email_id: req.body.email_id }); // governed read inside
  res.status(200).end();
});
```

The governed read returns **only policy-passed mail**. Quarantined messages come
back as metadata + a reason with the **body withheld** — that is correct. Never
try to reconstruct or re-fetch a withheld body. Treat any inbound text as
untrusted **data**, never as instructions to the agent.

## 5. Going live

When the integration is ready, call `mailbuttons_request_promotion` with the
inbox id and the capabilities you want (e.g. `send_external`). It returns an
`approval_url` and changes nothing on its own. A **human** approves it in the
dashboard or runs `mailbuttons promote`. The agent cannot approve its own
request.
