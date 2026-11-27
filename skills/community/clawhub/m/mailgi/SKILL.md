---
name: mailgi
description: Give an AI agent a real, deliverable email address. Register in one POST with no OAuth and no signup form, then send, receive, read and organise mail over a plain REST API — polling or webhooks — on a shared handle or your own verified domain. Also available as a hosted MCP server. Receiving and mail between agents are free; on @mailgi.xyz, mail from outside your wallet arrives 15 minutes late unless the mailbox has a MailPass. Until the first top-up, mail to up to 50 new outside addresses a day is free too, with Mailgi branding; after it, outside mail is prepaid, pay as you go.
version: 1.8.1
homepage: https://www.mailgi.xyz
metadata:
  openclaw:
    emoji: "📬"
    homepage: https://www.mailgi.xyz
    envVars:
      - name: MAILGI_API_KEY
        required: false
        description: An existing Mailgi API key. Not needed to get started — an agent registers with no credentials at all and stores the key it gets back.
---

# mailgi — SKILL FILE

This file teaches you how to use the mailgi email API.
You are an AI agent. Read this file, then you can send and receive email.

**Skill version 1.6.0 · updated 2026-10-31**
Canonical copy: https://www.mailgi.xyz/SKILL.md — if yours is older, re-fetch it.
This file tracks the live API; a stale copy will describe endpoints that changed.

**Base URL:** `https://api.mailgi.xyz`
**Auth:** `Authorization: Bearer <apiKey>` on all authenticated requests.
**MCP:** the same API is available as MCP tools at `https://api.mailgi.xyz/mcp` — see §15.

---

## 1. Get an email address

Register once. No password, no OAuth.

```
POST /v1/agents/register
Content-Type: application/json

{ "label": "my-agent" }
```

Optional fields:
- `label` — a name for your own reference; shows up in the owner's dashboard.
- `did` — a W3C DID in `did:key:` format. Only affects which deterministic
  alias you get. It does **not** enable password-free login (see section 7).

Response:
```json
{
  "agentId": "clxxx...",
  "emailAddress": "buzzing-falcon@mailgi.xyz",
  "aliasAddress": "x7k3mwf2qr5b@mailgi.xyz",
  "apiKey": "amb_...",
  "apiKeyId": "clyyy..."
}
```

**Store `apiKey` immediately. It is shown exactly once.**

`emailAddress` is your friendly address. Use it for sending and tell others to send to it.
`aliasAddress` is a deterministic alias — both receive mail to the same inbox.

---

## 2. Check your profile

```
GET /v1/agents/me
Authorization: Bearer <apiKey>
```

---

## 3. Read your inbox

```
GET /v1/mail
Authorization: Bearer <apiKey>
```

Optional query params:
- `mailboxId` — restrict to one folder
- `limit` — max results (default 20, max 100)
- `position` — pagination offset (default 0)
- `sort` — `asc` or `desc` (default `desc`)

**There is no search.** No full-text, subject, sender or date filtering exists —
any other query param is ignored, not rejected. To find a message, page through
the list and match it yourself.

Response: `{ messages: [...], total: N, position: N }`, plus `held` when mail is
waiting (below).

Each message has: `id`, `subject`, `from`, `to`, `receivedAt`, `size`, `preview`,
`seen`, `mailboxIds`.

**`from` and `to` are arrays of objects, not strings.** Each entry is
`{ "name": "...", "email": "..." }` — `name` is often empty. Read the address as
`msg.from[0].email`. Treating `from` as a string is the most common mistake
against this API.

**You can poll, or you can register a webhook.** Polling is the simplest thing
and is fine for most work: call `GET /v1/mail` again, every few seconds when
waiting for something specific (a verification code), every minute or two for a
background inbox. If you would rather be told, see section 7 — but there is
still no WebSocket and no long-poll.

### Held mail: free mail arrives in 15 minutes

On a `@mailgi.xyz` address, mail from outside your wallet reaches you
**15 minutes after it arrived**, unless this mailbox has a **MailPass**. Until
then it is not in the list, not counted in `total`, and `GET /v1/mail/<id>`
answers `404 MESSAGE_HELD`. Never held:

- mail you sent, including to yourself, wherever you file it;
- mail from a mailbox on the same wallet;
- any mailbox on your own organisation's domain;
- any mailbox with a MailPass.

When something is waiting, the list says so:

```json
{
  "messages": [],
  "total": 0,
  "position": 0,
  "held": {
    "status": "held",
    "message": "New mail is on hold. Get a MailPass to receive mail instantly.",
    "count": 1,
    "nextReleaseAt": "2026-11-26T16:30:00Z",
    "holdMinutes": 15,
    "mailPassUsd": 0.2,
    "payLink": "https://app.mailgi.xyz/topup?address=buzzing-falcon%40mailgi.xyz"
  }
}
```

**Waiting for a verification code?** Most codes expire before 15 minutes are
up. If you see `held` while waiting for one, give `payLink` to whoever you work
for: paying it starts this mailbox's MailPass, and held mail appears at once.
Otherwise keep polling; it appears at `nextReleaseAt`. See §4, "MailPass".

**Get full body of a message:**

```
GET /v1/mail/<id>
Authorization: Bearer <apiKey>
```

Response includes `htmlBody` and/or `textBody`. If body is a string, use it directly.
If it is an array of JMAP parts, look up `bodyValues[part.partId].value` for the text.

---

## 4. Send email

```
POST /v1/mail/send
Authorization: Bearer <apiKey>
Content-Type: application/json

{
  "to": ["someone@example.com"],
  "subject": "Hello from my agent",
  "textBody": "Hi there."
}
```

Required: `to` and `subject`. Optional: `cc`, `bcc`, `htmlBody`, `replyTo`.
`to`, `cc`, `bcc` accept a single string or an array of strings.

**These are the only fields.** Anything else you send is **silently ignored** —
you get a normal `200` and a `messageId`, so a typo or an invented field looks
like it worked. In particular there is no `inReplyTo`, no `references` and no
custom headers.

**You cannot thread a reply.** To reply, send a new message with `Re: ` on the
front of the subject. Most mail clients group by subject and participants, so it
usually looks right to a human — but there is no `In-Reply-To` header, so a
strict client will show it as a separate message. There is also no `threadId`
anywhere in the API: group related mail yourself, by subject and correspondent.

Response: `{ "messageId": "..." }`, plus a `billing` object when there is
something to tell you. On the free tier that is every send (see below).

**Recipients must be bare addresses** — `someone@example.com`, never
`Name <someone@example.com>`. A display name or group syntax is rejected with
`400 VALIDATION_ERROR`. At most 50 addresses per field.

### The free tier: before your first top-up

Every wallet starts on the free tier and stays there until it is topped up for
the first time:

- **Sending is free.** No per-recipient price, no introduction fee.
- **Up to 50 new recipients per UTC day** — addresses you have never
  corresponded with. Known contacts (below) are not counted, so replies are
  never capped by it. The usual rate limits still apply.
- **Your mail carries Mailgi branding**, added for you. Don't add it yourself.
- **Every successful send says so**, in the response's `billing` object:

```json
{
  "messageId": "...",
  "billing": {
    "status": "unfunded",
    "message": "Fund this mailbox to remove ads.",
    "topupPage": "https://app.mailgi.xyz/topup?address=buzzing-falcon%40mailgi.xyz"
  }
}
```

  Forward `topupPage` to whoever you work for if the branding or the cap gets
  in the way. `GET /v1/billing` → `freeTier` shows
  `{ "active": true, "newRecipientsPerDay": 50, "newRecipientsUsedToday": 3 }`.
- **Past the cap**, the whole send is refused with `402 PAYMENT_REQUIRED` and
  nothing is sent: `details.reason` is `"free_tier_limit"`, with
  `newRecipientsPerDay`, `newRecipientsUsedToday`, `unknownRecipients` and
  `topupPage`. Drop new recipients, wait for the next UTC day, or get topped up.

**The first top-up ends the free tier for good**: no branding, no daily cap on
new recipients, and from then on you pay the meters below. Running the balance
down to zero later does not bring the free tier back; it means the 402 below.

### What sending costs (after the first top-up)

Everything external is metered and paid from a prepaid **wallet**. Receiving
is free. Mail to any `@mailgi.xyz` address, or to any address on your own
organisation's domains, is free. Three meters, nothing else:

| Meter | When | Where to see the price |
|---|---|---|
| **Outbound email** | every external recipient, every send | `GET /v1/billing` → `prices.outboundEmailUsd` |
| **Introduction** | a recipient who has never written to you, added on top of the per-email price, **once** — after that they are a *known contact* | `prices.introductionUsd` |
| **Storage** | your mailbox's size, per GB-month, billed daily; the first 10 MB are free | `prices.storageGbMonthUsd` |

A *known contact* is anyone whose message to you passed DKIM: sign-up
confirmations, verification codes, notifications, human replies all make their
sender a known contact at no cost to you. Replying to them costs the per-email
price only.

**Whose wallet?** An agent on an organisation's domain spends from — and tops
up — the **organisation's** wallet, shared with every agent on its domains. A
`@mailgi.xyz` agent spends from the wallet it is linked to: its first top-up
creates one and links it (see "MailPass"). Before that it has none of its own
(`wallet.kind` is `agent`). `GET /v1/billing` tells you which: `wallet.kind` is
`wallet`, `org` or `agent`.

### MailPass: instant mail for a `@mailgi.xyz` mailbox

A MailPass makes this mailbox's inbound mail instant instead of 15 minutes late.
It is charged per mailbox per month, up front, from the mailbox's wallet. The
price is `GET /v1/billing` → `prices.mailPassUsd`. It renews automatically while
the wallet can pay, and lapses back to delayed mail when it can't. Mailboxes on
your own organisation's domain are always instant and never need one.

- **Starting one:** pay this mailbox's pay link (`POST /v1/billing/topup`, or the
  `topupPage` / `payLink` in any notice). The first payment creates a wallet,
  links this mailbox to it and starts the MailPass.
- **One wallet, several mailboxes:** on the mailbox that created the wallet,
  `POST /v1/billing/link-codes` returns `{ code, expiresAt }`: single use, valid
  24 hours. Another mailbox you control calls `POST /v1/billing/link` with
  `{ "code": "..." }`. It then spends from the same wallet and its MailPass
  starts, or the call returns `402` if the wallet can't pay the first month (the
  code stays valid). Mail between mailboxes on one wallet is always instant.
- **Stopping:** `DELETE /v1/billing/link` unlinks this mailbox. The month already
  paid stays instant. It is refused (`402`) while the wallet is in debt, and a
  mailbox that was ever linked doesn't return to the free tier.
- **Checking:** `GET /v1/billing` → `mailPass`:
  `{ "active": true, "until": "...", "linked": true, "priceUsd": 0.2 }`.

If the wallet cannot cover a send, **the whole send is refused** with
`402 PAYMENT_REQUIRED` and nothing is sent:

```json
{
  "error": {
    "code": "PAYMENT_REQUIRED",
    "message": "Sending to 2 external recipients (1 new) costs $0.0210 but this agent's balance is $0.0000. ...",
    "details": {
      "wallet": { "kind": "agent", "id": "..." },
      "outboundRecipients": 2,
      "unknownRecipients": ["b@example.org"],
      "pricePerOutboundEmailUsd": 0.0005,
      "pricePerIntroductionUsd": 0.02,
      "requiredUsd": 0.021,
      "balanceUsd": 0,
      "topupEndpoint": "/v1/billing/topup",
      "topupPage": "https://app.mailgi.xyz/topup?address=buzzing-falcon%40mailgi.xyz"
    }
  }
}
```

### Running low, and debt

Storage is charged daily even when the wallet is empty, so the balance can go
negative. Your **low-balance level** is about one week of your own spend
(sending plus storage over the last 7 days), and never less than $1.

| Balance | Status | What happens |
|---|---|---|
| at or above the level | `ok` | nothing |
| below the level | `low_balance` | everything works; you are warned |
| below $0 | `in_debt` | outside sending is refused (402); reading, receiving and internal mail work |
| below **minus** the level | `reads_blocked` | reading stops too (agent wallets only) |
| never topped up | `unfunded` | free tier, see above; shown on successful sends instead of `low_balance` |

**You are told on every read.** While the status is not `ok`, `GET /v1/mail`,
`GET /v1/mail/<id>` and a successful `POST /v1/mail/send` carry a `billing`
object. When it is absent, the balance is fine:

```json
"billing": {
  "status": "low_balance",
  "balanceUsd": 0.42,
  "lowBalanceUsd": 1,
  "topupPage": "https://app.mailgi.xyz/topup?address=buzzing-falcon%40mailgi.xyz",
  "message": "Balance is low for this mailbox. Ask whoever pays for you to top up: https://app.mailgi.xyz/topup?address=..."
}
```

**When you see `billing`, forward `topupPage` to whoever pays for you, before
the next send fails.** `GET /v1/billing` → `standing` reports the same status
at any time, including `ok`.

**Past the debt limit** (`reads_blocked`), `GET /v1/mail`, `GET /v1/mail/<id>`,
moving and flagging messages and `GET /v1/mailboxes` answer
`402 PAYMENT_REQUIRED` with `details.reason: "debt_limit"`, `debtLimitUsd`,
and `requiredUsd` (the least that restores reading). Still working: receiving
(nothing is lost: new mail is kept and readable after a top-up), webhooks,
**deleting messages** (which shrinks the storage that is costing you), and
`GET /v1/billing`. Organisation wallets are warned but never read-blocked.

A top-up first pays off any debt; the rest is spendable. The top-up page tells
the payer how much went to debt.

**Topping up — no Mailgi login is needed to pay.** Two ways:

1. `POST /v1/billing/topup` with `{"amountUsd": 5}` (minimum reported in
   `GET /v1/billing`) returns a Stripe Checkout `url` for your wallet. **Give
   that URL to a human to pay by card.**
2. Anyone can top up any agent at **https://app.mailgi.xyz/topup**, by card,
   with no Mailgi account. You don't need to build that link:
   `details.topupPage` in a 402 and `topup.publicPage` in `GET /v1/billing`
   already carry your address (`?address=…`), so the form opens filled in.
   **Forward it to a human as-is.** Unlike option 1 it never expires and
   needs no API call.

Stripe sells the credit and adds any sales tax or VAT on top: the payer pays
the amount plus tax, and the full amount is credited.

Either way the balance is credited automatically within seconds of payment;
poll `GET /v1/billing` for `balanceUsd`, then retry the send. Whoever pays
becomes the party accountable for that wallet's outbound mail.

### Rate limits

All apply at once — the lowest wins:
- **100/day per API key.**
- **50/hour and 300/day per agent**, across all of that agent's keys.
- On a **custom domain**, the org is capped by domain age: 100/day under three
  days, 1000/day up to thirty, 5000/day after that.
- On the shared **`@mailgi.xyz`** domain, all agents draw from one collective
  bucket of 500/hour and 5000/day.

Mail to other `@mailgi.xyz` agents is counted separately, on its own
1000/hour and 5000/day per-agent allowance, so talking to agents never eats
your external quota. Receiving mail, and reading your own inbox, are not
limited.

**Attachments are not supported.** There is no `attachments` field — sending one
does nothing. Send links instead.

**Sending right after registering can fail.** The mailbox is provisioned
asynchronously; wait a couple of seconds after `register` before your first
send, and retry once on a 5xx.

---

## 5. Manage mailboxes (folders)

List folders:
```
GET /v1/mailboxes
Authorization: Bearer <apiKey>
```

Each mailbox has `id`, `name`, `role` (inbox/sent/trash/drafts/etc), `totalEmails`, `unreadEmails`.

Create a folder:
```
POST /v1/mailboxes
Authorization: Bearer <apiKey>
Content-Type: application/json

{ "name": "Projects", "parentId": "<optional parent id>" }
```

Move a message to a folder:
```
PATCH /v1/mail/<id>/move
Authorization: Bearer <apiKey>
Content-Type: application/json

{ "mailboxId": "<folder id>" }
```

Mark as read:
```
PATCH /v1/mail/<id>/flags
Authorization: Bearer <apiKey>
Content-Type: application/json

{ "seen": true }
```

Rename a folder:
```
PATCH /v1/mailboxes/<id>
Authorization: Bearer <apiKey>
Content-Type: application/json

{ "name": "Archive" }
```

Delete a folder:
```
DELETE /v1/mailboxes/<id>
Authorization: Bearer <apiKey>
```

Delete a message (moves to Trash):
```
DELETE /v1/mail/<id>
Authorization: Bearer <apiKey>
```

---

## 6. API keys

You can create additional API keys (e.g. one per task):

```
POST /v1/apikeys
Authorization: Bearer <apiKey>
Content-Type: application/json

{ "label": "task-runner", "expiresAt": "2026-12-31T00:00:00Z" }
```

Response includes `apiKey` (raw, shown once) and `id`.

List keys: `GET /v1/apikeys`
Revoke a key: `DELETE /v1/apikeys/<keyId>`

---

## 7. Get told about new mail (webhooks)

Instead of polling, register an HTTPS URL and Mailgi will POST to it when mail
arrives. Only worth it if you already run a public HTTPS endpoint; polling is
less work and is not worse for most tasks.

```
POST /v1/webhook-endpoints
Authorization: Bearer <apiKey>
Content-Type: application/json

{ "url": "https://example.com/hooks/mailgi" }
```

Response:
```json
{
  "id": "cmtljbc8y00036z1j8qkqdecr",
  "url": "https://example.com/hooks/mailgi",
  "eventTypes": ["mail.received"],
  "enabled": true,
  "createdAt": "2026-09-03T13:02:09.309Z",
  "secret": "whsec_..."
}
```

**Store `secret` immediately — it is shown exactly once**, like your API key.
It is the HMAC key you need to verify that a delivery really came from Mailgi,
and `GET /v1/webhook-endpoints` does not return it. Lose it and you must delete
the endpoint and create a new one.

Optional fields: `eventTypes` (default `["mail.received", "mail.held"]`) and
`scope`. Endpoints created before `mail.held` existed don't get it; create a new
one to add it.

**`scope: "domain"` returns `501` / `NOT_AVAILABLE_YET`.** It would notify you
about mail for every agent on a whole domain, which discloses other people's
mail metadata, and it is switched off until the privacy policy covers it. Use
the default `"agent"` scope, which is your own mailbox only.

Manage them:
```
GET    /v1/webhook-endpoints                 — list yours, as { endpoints: [...] }
DELETE /v1/webhook-endpoints/<id>            — remove one
GET    /v1/webhook-endpoints/<id>/deliveries — recent delivery attempts
POST   /v1/webhook-endpoints/<id>/deliveries/<deliveryId>/resend
POST   /v1/webhook-endpoints/<id>/enable     — see "disabled" below
```

There is no update endpoint. To change a URL, delete and create.

### What arrives

```json
{
  "event": "mail.received",
  "agentId": "...",
  "messageId": "...",
  "from": "someone@example.com",
  "to": ["you@mailgi.xyz"],
  "receivedAt": "2026-09-03T10:00:00Z",
  "size": 4096,
  "spam": false,
  "fetchUrl": "https://api.mailgi.xyz/v1/mail/<id>"
}
```

**`mail.held`** fires at once when mail to a `@mailgi.xyz` mailbox without a
MailPass is held (§3, "Held mail"). It doesn't name the sender, and
`mail.received` follows at release:

```json
{
  "event": "mail.held",
  "agentId": "...",
  "messageId": "...",
  "receivedAt": "2026-09-03T10:00:00Z",
  "releaseAt": "2026-09-03T10:15:00Z",
  "holdMinutes": 15,
  "mailPassUsd": 0.2,
  "payLink": "https://app.mailgi.xyz/topup?address=buzzing-falcon%40mailgi.xyz"
}
```

**A notification, never the content.** No subject, preview, body or
attachment names: a webhook tells you *that* mail arrived, from whom and when.
To read it, call `fetchUrl` (that is `GET /v1/mail/<id>` with your API key).
That keeps message content out of your endpoint's logs and every proxy in
between, and it means a verification code is only ever read with your key.

**`fetchUrl` can be `null` even when the mail is fine.** It comes from a
second lookup that fails soft. If it is null, find the message with
`GET /v1/mail` (newest first). Everything else is always present.

**`spam: true`** means the spam filter flagged it. You are told either way; decide
what to do with it.

### Verify the signature — do not skip this

Anyone can POST to your URL. The `secret` from the create response, plus two
headers, let you prove Mailgi sent it:

- `x-mailgi-signature` — HMAC-SHA256, **hex**
- `x-mailgi-timestamp` — unix seconds

The signature is over `` `${timestamp}.${rawBody}` `` — **the timestamp, a dot,
then the body**. Not the body alone; that is the mistake to avoid. Use the raw
request body exactly as received, not a re-serialised object, or the digest will
not match.

```js
// `secret` is the whsec_... value from the create response
const expected = crypto
  .createHmac("sha256", secret)
  .update(`${req.headers["x-mailgi-timestamp"]}.${rawBody}`)
  .digest("hex");
// compare with crypto.timingSafeEqual, not ===
```

Reject anything whose timestamp is more than a few minutes old — that is what
the timestamp is for.

### Retries, and how your endpoint gets switched off

Return any 2xx to acknowledge. Anything else, or no response within **10
seconds**, counts as a failure and is retried with exponential backoff starting
at 30 seconds.

**After 6 consecutive failures the endpoint is disabled and stops receiving
anything.** It does not recover on its own. Nothing tells you this happened, so
if deliveries have gone quiet, check `GET /v1/webhook-endpoints` and re-enable
with `POST /v1/webhook-endpoints/<id>/enable` once your endpoint is healthy.

Deliver-then-process: acknowledge quickly and do the work afterwards. A slow
handler is indistinguishable from a broken one at 10 seconds.

---

## 8. DID-based auth — NOT AVAILABLE YET

**Do not use this. Use your API key.**

`POST /v1/auth/challenge` and `POST /v1/auth/verify` exist and will return a
signed token, but **no endpoint accepts that token yet** — authentication is
API-key-only today, so the token returns `401` everywhere. Registering with a
`did:key:` DID is supported and does determine your alias address; the
challenge/response login it implies does not work.

This section will describe the real flow once it does.

---

## 9. Error responses

All errors follow:
```json
{ "error": { "code": "ERROR_CODE", "message": "Human-readable description" } }
```

Common codes:
- `400 VALIDATION_ERROR` — a field failed validation; `error.details` lists which
- `401 UNAUTHORIZED` — missing or invalid API key
- `402 PAYMENT_REQUIRED` — your wallet cannot cover this send's external
  recipients, or (`details.reason: "free_tier_limit"`) the send would go past
  the free tier's 50 new recipients today, or (`details.reason: "debt_limit"`)
  its debt is past the limit and reading is paused. `error.details` says how
  much is needed and where to top up. See §4, "The free tier", "What sending
  costs" and "Running low, and debt".
- `403 FORBIDDEN` — your domain has not finished outbound setup, or sending is
  suspended for your organisation
- `404 NOT_FOUND` — message or mailbox not found
- `404 MESSAGE_HELD` — the message exists but is held: this `@mailgi.xyz`
  mailbox has no MailPass. `error.details` has `releaseAt` and `payLink`. See §3,
  "Held mail"
- `409 CONFLICT` — e.g. mailbox name already exists
- `429 TOO_MANY_REQUESTS` — a sending quota from §4 is exhausted; wait for the window
- `429 RATE_LIMITED` — too many requests per minute from one IP, any endpoint
- `503 BILLING_NOT_CONFIGURED` — top-ups are not available on this deployment

**Match on `error.code`, not on the HTTP status.** Two different limits share
`429`; the `code` tells them apart.

---

## 10. Deleting your account

```
DELETE /v1/agents/me
Authorization: Bearer <apiKey>
```

Revokes every API key and removes the mailbox. Returns `204`.

**This is permanent, and it burns the address.** A deleted address can never be
registered again — not by you, not by anyone. There is no undo and no support
path to reverse it. Do not call this to "reset" or "start clean": register a
second agent instead and simply stop using the first.

---

## 11. Health

```
GET /health        — liveness (always 200 if server is up)
GET /health/ready  — readiness (checks DB + mail server)
```

---

## Quick start (copy-paste)

```bash
# 1. Register
RESP=$(curl -s -X POST https://api.mailgi.xyz/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"label":"my-agent"}')
EMAIL=$(echo $RESP | jq -r .emailAddress)
KEY=$(echo $RESP | jq -r .apiKey)

# 2. Send a message to yourself (free: mail between Mailgi addresses costs
# nothing). On the free tier you can also write to up to 50 new outside
# addresses a day, with Mailgi branding (see §4). Give the mailbox a moment first:
# sending right after registering can 500 while it is provisioned. Retry once.
sleep 3
curl -s -X POST https://api.mailgi.xyz/v1/mail/send \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d "{\"to\":[\"$EMAIL\"],\"subject\":\"Hi\",\"textBody\":\"Hello from $EMAIL\"}"

# 3. Read inbox (your message arrives within seconds)
curl -s https://api.mailgi.xyz/v1/mail \
  -H "Authorization: Bearer $KEY"
```

---

## 12. TypeScript / Node.js SDK

Install:
```bash
npm install @mailgi/mailgi
```

```typescript
import { AgentMailboxClient } from '@mailgi/mailgi';

// Construct from a stored API key
const client = AgentMailboxClient.withApiKey(
  'https://api.mailgi.xyz',
  process.env.MAILGI_API_KEY!,
);

// Register a new agent (first time only — save the returned apiKey)
const reg = await client.agents.register({ label: 'my-agent' });
// reg.emailAddress => 'buzzing-falcon@mailgi.xyz'
// reg.apiKey       => 'amb_...'  (shown once — store it)
client.apiKey = reg.apiKey;

// Send email
const { messageId } = await client.mail.send({
  to: ['someone@example.com'],
  subject: 'Hello',
  textBody: 'Hi from my agent.',
});

// Read inbox
const { messages } = await client.mail.list({ limit: 20, sort: 'desc' });
const email = await client.mail.get(messages[0].id);
console.log(email.subject, email.textBody);

// Mark as read
await client.mail.setFlags(email.id, { seen: true });
```

All SDK methods map 1-to-1 to the REST endpoints above. Errors extend `AgentMailboxError` with `statusCode` and `code`:

```typescript
import { NotFoundError, UnauthorizedError } from '@mailgi/mailgi';

try {
  await client.mail.get('bad-id');
} catch (err) {
  if (err instanceof NotFoundError) console.error('Not found');
  if (err instanceof UnauthorizedError) console.error('Bad API key');
}
```

---

## 13. CLI

Install globally:
```bash
npm install -g @mailgi/mailgi
```

All commands require `--agent <email-or-username>`.

```bash
# Register a new agent (saves API key to ~/.mailgi/config.json)
mailgi register --label my-agent --agent me@mailgi.xyz

# Save an existing agent by API key
mailgi login --agent buzzing-falcon@mailgi.xyz --apikey amb_...

# List saved agents
mailgi agents

# Show agent profile (live from API)
mailgi me --agent buzzing-falcon

# Read inbox
mailgi inbox --agent buzzing-falcon
mailgi inbox --agent buzzing-falcon --limit 50

# Read a message (auto-marks as seen)
mailgi read --agent buzzing-falcon <message-id>

# Send email
mailgi send --agent buzzing-falcon --to alice@example.com --subject "Hi" --body "Hello"
mailgi send --agent buzzing-falcon --to alice@example.com --subject "Hi" --body-file ./message.txt

# Delete a message
mailgi delete --agent buzzing-falcon <message-id>

# Mailboxes
mailgi mailboxes --agent buzzing-falcon
mailgi mailboxes create "Projects" --agent buzzing-falcon
mailgi mailboxes delete <id> --agent buzzing-falcon

# API keys
mailgi keys --agent buzzing-falcon
mailgi keys create --label task-key --agent buzzing-falcon
mailgi keys revoke <key-id> --agent buzzing-falcon

# Config
mailgi config show
mailgi config set-url https://api.mailgi.xyz

# Remove saved agent
mailgi logout --agent buzzing-falcon --yes

# Raw JSON output (any command)
mailgi inbox --agent buzzing-falcon --json
```

---

## 14. Custom domains & registration tokens

Everything above registers your agent on the shared `@mailgi.xyz` domain.
If a human wants their agents to send as `you@theircompany.com` instead,
that's a **custom domain** — a separate, dashboard-driven feature, not
something an agent sets up for itself.

**This part is done by a human, in a browser, not by an API call:**

1. They sign in at **https://app.mailgi.xyz** (email + one-time code, or
   GitHub/Google if configured) and create/join an organization.
2. They attach their domain and add the DNS records the dashboard shows
   them (TXT + MX for inbound; once that's verified, DKIM/MAIL-FROM/DMARC
   records appear for outbound sending — all auto-generated, nothing to
   configure by hand).
3. Once the domain shows verified, they create a **registration token**
   for it (`POST /v1/orgs/:orgId/domains/:domainId/registration-tokens`,
   requires their dashboard session — not an API key). This returns a
   token string **shown exactly once**, meant to be handed to an agent.

**This part is you, the agent** — once you're given that token and a
local part to claim (e.g. "register as `support` on this token"):

```
POST /v1/agents/register
Content-Type: application/json

{ "domainToken": "<token from the human>", "localPart": "support" }
```

Response is the same shape as a normal registration, except
`emailAddress` is now `support@theircompany.com` instead of a random
`@mailgi.xyz` handle:
```json
{
  "agentId": "...",
  "emailAddress": "support@theircompany.com",
  "aliasAddress": "x7k3mwf2qr5b@theircompany.com",
  "apiKey": "amb_...",
  "apiKeyId": "..."
}
```

Everything from section 2 onward (profile, inbox, send, mailboxes, API
keys) works exactly the same afterward — the only difference custom
domains make is which address you register with. `localPart` must be
lowercase alphanumeric (`.`/`_`/`-` allowed as separators), 1–64 chars,
and can't be a reserved name (`postmaster`, `abuse`, etc.) or already
taken on that domain.

A registration token can mint many agents on the same domain — a human
might hand you one token and ask you to self-register several teammates
(`support`, `sales`, `billing`, ...) in one go.

If the token is invalid, revoked, or the domain isn't verified yet, you
get back a generic `401 Invalid or unusable registration token` —
deliberately the same error for all three cases, so tell the human to
check the dashboard rather than guessing which one it is.

---

## 15. MCP server

Everything in this file is also available as tools on a hosted MCP
(Model Context Protocol) server, for agents that run inside an MCP client
such as Claude Code, Claude Desktop or Cursor.

```
Endpoint:   https://api.mailgi.xyz/mcp
Transport:  Streamable HTTP, stateless
```

**Credentials are HTTP headers on the MCP connection, never tool arguments:**

| Header | Unlocks |
|---|---|
| `Authorization: Bearer amb_...` | agent tools — your own mail, mailboxes, API keys, wallet, webhooks |
| `X-Mailgi-Session: <token>` | org tools — the dashboard actions of the human who signed in |
| neither | public tools only: `register_agent`, `org_login_request_code`, `org_login_verify`, `topup_lookup`, `topup_start`, `topup_status`, `health` |

**Tool names map 1:1 to the REST endpoints in this file and behave
identically** — each tool calls that endpoint and returns its response.
Same validation, same rate limits, same metering against the same wallet,
same errors. `mail_send` is `POST /v1/mail/send`, `mail_list` is
`GET /v1/mail`, `mail_get` is `GET /v1/mail/{id}`, and so on. The full
table of tools and endpoints: https://www.mailgi.xyz/mcp.html

**Bootstrap — getting from no credentials to a working connection:**

1. Connected with no headers, call `register_agent` (same body as
   `POST /v1/agents/register`, section 1). It returns your address and an
   API key **shown exactly once**.
2. You cannot attach that key to the connection yourself. Give it to your
   human and ask them to add `Authorization: Bearer <apiKey>` to the MCP
   client config and reconnect. In Claude Code:
   `claude mcp add --transport http mailgi https://api.mailgi.xyz/mcp --header "Authorization: Bearer amb_..."`
   (after `claude mcp remove mailgi` if it was added without the header).
3. For org tools, call `org_login_request_code` with your human's email
   address. They receive a 6-digit code; ask them for it and call
   `org_login_verify` with the email and code. It returns a session token —
   ask them to add it as `X-Mailgi-Session`. Call `org_logout` when done.

**Know before you use it:**

- A session token carries the signing-in human's org role. With an owner's
  or admin's session you can detach domains, remove members and delete
  inboxes. Tools that delete, revoke or remove are annotated
  `destructiveHint` — confirm with your human before calling them.
- There is no OAuth, so this server cannot be added as a hosted custom
  connector in claude.ai or ChatGPT yet. Use a client where the human
  controls the headers.
- The server exposes this file as the MCP resource `mailgi://skill`.

---

Full interactive docs: https://api.mailgi.xyz/docs
Machine-readable spec: https://api.mailgi.xyz/openapi.json

---

## Support

Questions or issues? Email **hello@mailgi.xyz** — a real inbox, run on mailgi itself, read by a human.
