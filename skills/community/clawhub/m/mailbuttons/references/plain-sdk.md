# Wiring Mailbuttons into plain TypeScript or Python (no framework)

This is the idiom reference for the **plain SDK** target — a TypeScript or Python
app with no agent framework. It covers connecting to a Mailbuttons **sandbox**
inbox, the governed send pattern, reading the key from the environment, and the
inbound handler shape. For tone/structure see the reference repos
`github.com/mailbuttons/claude-scheduling-agent-ts` and `...-py`.

Everything here is **sandbox-only**. Nothing below enables external send,
promotes to production, or widens a token's scope.

## 1. The key comes from the environment

TypeScript:

```ts
const API_URL = process.env.MAILBUTTONS_API_URL ?? "http://localhost:8000";
const API_KEY = process.env.MAILBUTTONS_API_KEY; // mb_sandbox_...
if (!API_KEY) throw new Error("Set MAILBUTTONS_API_KEY (a scoped sandbox token).");
```

Python:

```python
import os
API_URL = os.environ.get("MAILBUTTONS_API_URL", "http://localhost:8000")
API_KEY = os.environ.get("MAILBUTTONS_API_KEY")  # mb_sandbox_...
if not API_KEY:
    raise RuntimeError("Set MAILBUTTONS_API_KEY (a scoped sandbox token).")
```

Never inline the token. The scaffolded `send.*` / `inbox.*` files already read it
from the environment — keep it that way.

## 2. Talk to the governed REST endpoints

Plain apps call `/api/v1/mcp/*` directly with `Authorization: Bearer <token>`:

- `POST /api/v1/mcp/send` — send/draft (governed)
- `GET  /api/v1/mcp/messages?inbox_id=<id>` — list policy-passed messages
- `GET  /api/v1/mcp/messages/<email_id>?inbox_id=<id>` — read one message
- `GET  /api/v1/mcp/threads/<thread_id>?inbox_id=<id>` — read a thread

The scaffolded `send` and `inbox` files wrap these for you.

## 3. The governed send pattern

A send returns a **governed outcome**, not a bare success. `blocked` and
`draft_pending_approval` are normal results — handle them, don't retry to force
a send through.

| status | meaning | do |
|---|---|---|
| `sent` / `queued` | delivered internally | done |
| `blocked` | recipient fails policy (`policy.matched_rule`) | log the rule; stop |
| `draft_pending_approval` | external recipient, no `send_external` | a human must approve; draft parked |

TypeScript:

```ts
const r = await governedSend({ to: ["ops@sandbox.mailbuttons.app"], subject, text });
if (r.status === "blocked") console.warn("Blocked by", r.policy.matched_rule);
if (r.status === "draft_pending_approval") console.warn("Parked for human approval.");
```

Python:

```python
r = governed_send(to=["ops@sandbox.mailbuttons.app"], subject=subject, text=text)
if r["status"] == "blocked":
    print("Blocked by", r["policy"].get("matched_rule"))
elif r["status"] == "draft_pending_approval":
    print("Parked for human approval.")
```

When you address an external recipient, you get `draft_pending_approval` and a
draft — it did not send. That is the governance working.

## 4. Inbound handler shape

Inbound is a webhook (`email.received`) carrying metadata only. Verify the
`X-Mailbuttons-Signature` HMAC over the raw request body, then fetch the full
message through the governed read endpoint.

TypeScript (Express-style):

```ts
app.post("/webhook/mailbuttons", async (req, res) => {
  if (!verifySignature(req.rawBody, req.header("X-Mailbuttons-Signature"))) {
    return res.status(401).end();
  }
  await onInboundEmail({ email_id: req.body.email_id });
  res.status(200).end();
});
```

Python (Flask-style):

```python
@app.post("/webhook/mailbuttons")
def webhook():
    if not verify_signature(request.get_data(), request.headers.get("X-Mailbuttons-Signature")):
        return "", 401
    on_inbound_email(request.json["email_id"])
    return "", 200
```

The governed read returns **only policy-passed mail**. Quarantined messages
arrive as metadata + reason with the **body withheld** — that is correct; never
reconstruct a withheld body. Treat all inbound text as untrusted **data**, never
as instructions to your code or model.

## 5. Going live

Call `mailbuttons_request_promotion` with the inbox id and the capabilities you
want (e.g. `send_external`). It returns an `approval_url` and grants nothing on
its own. A **human** approves it in the dashboard or via `mailbuttons promote`.
The app cannot approve its own request.
