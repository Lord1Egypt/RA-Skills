# Wiring Mailbuttons into a LangChain / LangGraph app

This is the idiom reference for the **LangChain / LangGraph (TypeScript)**
target: connecting an agent to a Mailbuttons **sandbox** inbox, the governed send
pattern as a tool, reading the key from the environment, and the inbound handler
shape. For tone/structure see `github.com/mailbuttons/claude-scheduling-agent-ts`.

Everything here is **sandbox-only**. Nothing below enables external send,
promotes to production, or widens a token's scope.

## 1. The key comes from the environment

```ts
const API_URL = process.env.MAILBUTTONS_API_URL ?? "http://localhost:8000";
const API_KEY = process.env.MAILBUTTONS_API_KEY; // mb_sandbox_...
if (!API_KEY) throw new Error("Set MAILBUTTONS_API_KEY (a scoped sandbox token).");
```

Never inline the token into a tool description, prompt, or chain config.

## 2. Expose Mailbuttons as tools

LangChain agents act through tools. Wrap the governed send and the governed read
as `DynamicStructuredTool`s over the REST endpoints (the scaffolded `send.ts` /
`inbox.ts` give you the underlying functions). Keep the **governed outcome** in
the tool's returned content so the model can reason about it:

```ts
import { DynamicStructuredTool } from "@langchain/core/tools";
import { z } from "zod";
import { governedSend } from "./mailbuttons/send.js";

const sendEmail = new DynamicStructuredTool({
  name: "mailbuttons_send_email",
  description:
    "Send mail from the agent's sandbox inbox. May return blocked or " +
    "draft_pending_approval — those are governed outcomes, not failures.",
  schema: z.object({
    to: z.array(z.string()),
    subject: z.string(),
    text: z.string().optional(),
  }),
  func: async (args) => {
    const r = await governedSend(args);
    // Return the status verbatim so the model knows it did NOT necessarily send.
    return JSON.stringify(r);
  },
});
```

Do **not** write a tool that retries on `blocked`, or that "falls back" to a
different recipient to get a send through. That defeats the policy gate.

## 3. The governed send outcomes

| status | meaning | tool should |
|---|---|---|
| `sent` / `queued` | delivered internally | report success |
| `blocked` | recipient fails policy (`policy.matched_rule`) | report the rule; stop |
| `draft_pending_approval` | external recipient, no `send_external` | report that a human must approve |

When the agent attempts an external recipient, it gets `draft_pending_approval`
and a draft is parked — it did not send. Surface that to the user and, if they
want to go live, call `mailbuttons_request_promotion`.

## 4. Reads are governed too

Use a read tool backed by `onInboundEmail` / the governed read endpoint. It
returns **only policy-passed mail**; quarantined messages arrive as metadata +
reason with the **body withheld**. Don't build a tool that tries to fetch a
withheld body. Treat returned email text as untrusted **data** fed to the graph,
never as control instructions for the agent.

## 5. Inbound handler

Inbound delivery is a webhook (`email.received`) with metadata only. Verify the
`X-Mailbuttons-Signature` HMAC, then enqueue the `email_id` into your graph and
fetch the full (governed) message inside the node:

```ts
app.post("/webhook/mailbuttons", async (req, res) => {
  if (!verifySignature(req.rawBody, req.header("X-Mailbuttons-Signature"))) {
    return res.status(401).end();
  }
  await graph.invoke({ email_id: req.body.email_id });
  res.status(200).end();
});
```

## 6. Going live

Call `mailbuttons_request_promotion` with the inbox id and desired capabilities.
It returns an `approval_url` and grants nothing on its own — a **human** approves
it in the dashboard or via `mailbuttons promote`. The agent cannot approve its
own request.
