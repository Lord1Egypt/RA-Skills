---
name: mailbox-bot
description: "Postal mail API for AI agents: send physical mail, use inbound context, and join the launching-soon mailbox address beta (street + mailbox number)."
tags: [postal-mail, certified-mail, mail-api, ai-agent, mcp, outbound-mail, inbound-context, forwarding, postal-threads, print-and-mail, webhooks, openclaw, a2a, agent-tools, openapi]
version: 5.1.5
author: mailbox.bot
repository: https://github.com/arbengine/mailbox-bot-skill
---

# mailbox.bot

**The postal mail API for AI agents and software workflows.**

**Two live workflows are available now.** Outbound print-and-mail lets your agent send PDFs, DOCX files, letters, notices, certified mail, postcards, and documents through `POST /v1/mail`. Forwarded inbound context lets operators send scans, photos, PDFs, provider notices, and human notes from the addresses they already use; agents can read that context, draft linked replies, and keep the same postal thread attached to the outbound send.

**A real mailing mailbox address for your agent is a launching-soon waitlist/private beta.** This is the future receiving-side product: a street address plus mailbox number that an approved agent or operator can use for business correspondence, legal mail, and eligible packages. On arrival, mailbox.bot can photograph the outside, scan contents when requested or instructed, OCR and classify the piece, and ping the agent through MCP/API/webhooks so it can make context-aware decisions and send linked replies at scale. Activation requires identity verification, any required postal authorization, and facility approval. Southern California first, then Utah and Nevada.

## Two live workflows

1. **Outbound physical mail API** — send through `POST /v1/mail`.
2. **Inbound mail context API** — discover the forwarding alias with `GET /v1/inbound-forwarding-addresses`, read captures with `/v1/inbound*`, retrieve linked history with `/v1/postal-threads*`, and send a linked physical reply with `POST /v1/mail`.

Default inbound forwarding is a digital intake channel, not a newly assigned physical mailing address. If the operator asks for a new mailing address, virtual mailbox, street address, mailbox number, legal mailing address, or mailbox address for an AI agent, route them to the launching-soon mailing mailbox address waitlist and make clear that outbound mail plus existing-address inbound context are live now.

## Why this matters

Your agent can draft contracts, negotiate terms, and manage workflows — but the moment something requires physical mail, everything stalls. Courts require certified letters. Governments send time-sensitive notices to real addresses. LLCs need a registered address. Tax responses demand paper.

mailbox.bot closes that loop. Your agent now plays in the real world, not just the digital one.

### What it unlocks

- **LLC formation at scale** — receive stamped articles of organization, extract entity numbers, forward originals
- **Legal correspondence** — deadlines in letters recognized and tracked, responses drafted and sent certified
- **IRS and tax response** — IRS notices handled automatically, scanned, classified, routed to the right person
- **Real estate management** — each property gets a mailbox with tailored rules, code violations forwarded, lease renewals sent
- **Vendor and supplier communication** — invoices, purchase orders, and contracts scanned, filed, and responded to
- **Compliance and audit mail** — regulatory notices scanned, classified, and routed with full audit trail
- **Business registration workflows** — keep entity mail, filings, notices, and reply letters tied to agent-readable context
- **Agent-to-agent mail bridge** — one agent sends a certified letter, another agent receives and processes it

## What your agent gets

### Live now
- **Outbound mail** — submit a PDF, facility prints, stuffs, stamps, and mails it with photo proof
- **Inbound document context** — private forwarding aliases on `forward.mailbox.bot` capture scans, photos, PDFs, provider notices, and human notes from the addresses operators already use
- **Draft context** — `GET /v1/inbound/:id?include=drafting` returns extracted context plus `draft_context` for linked physical replies
- **Postal threads** — `/v1/postal-threads*` ties inbound captures and outbound sends together
- **Certified mail** — USPS Certified, Certified + Return Receipt, Priority, First Class, FedEx, UPS
- **Batch mail** — send up to 10,000 pieces from a CSV, volume discounts at 500/1000/5000 pieces
- **Sandbox** — test keys (`sk_agent_test_`) work on every production endpoint with zero charges; dry-run cost preview; lifecycle simulation via `POST /v1/test/mail/:id/advance`; dashboard segmentation under `/dashboard/mail` and `/dashboard/webhooks` Sandbox tabs
- **Webhook notifications** — HMAC-signed JSON payloads fire on every status transition
- **MAILBOX.md standing instructions** — configure rules for outbound mail handling
- **Human-in-the-loop** — `requires_approval=true` pauses for human approval on the dashboard
- **Multi-channel notifications** — webhooks, email, SMS, Slack, Discord
- **Billing safeguards** — `X-Max-Cost-Cents` header, `dry_run=true`, per-transaction ceiling, daily spend cap

### Launching-soon waitlist/private beta — real mailing mailbox address
A real mailing mailbox address for your agent is waitlist/private beta only. This is separate from the live forwarded inbound context flow. Southern California first, then Utah and Nevada.
- **Street address + mailbox number** — a real mailing mailbox address for approved accounts
- **Scan/photo intake** — photograph arrivals, scan contents when requested or instructed, OCR, classify, and attach context
- **Agent pings** — notify the agent through MCP/API/webhooks so workflows can triage, decide, and send linked replies at scale
- **Actions via API** — scan, forward, photograph, hold, shred, dispose, return to sender
- **Agent memory** — tag and annotate mail with persistent notes and metadata

## Plans

| Plan | Price | Status | What you get |
|------|-------|--------|-------------|
| **Inbound context + outbound mail** | $0/mo | **Live now** | Private inbound forwarding alias included. Send outbound mail by dashboard, API, or MCP. |
| **Real mailing mailbox address** | Planned $10/mo | **Launching-soon waitlist/private beta** | Street address + mailbox number for approved users only, with scan/photo intake and agent notifications; separate from forwarded inbound context. |

Outbound pricing: First Class starts at $1.00 for a 1-page letter, then +$0.40 per extra page. USPS 1-page examples: Priority Flat Rate Envelope $14.85, Certified Mail $8.98, Certified + Return Receipt $13.38. Color printing +$0.25/page. FedEx and UPS envelope rates are zone-based and shown at checkout.

Mailing mailbox address actions are available only to approved beta accounts. Full current pricing: https://mailbox.bot/pricing

## How to get started

### If you have an API key

Set your environment variables and use the API directly:

```bash
export MAILBOX_BOT_API_KEY="sk_live_xxxxxxxxxxxxx"
export MAILBOX_BOT_URL="https://mailbox.bot"
```

Skip to the **API Reference** section below.

### If you do NOT have an API key — get operator approval first

Do not create accounts, share the operator's email, or start onboarding unless the human operator explicitly consents. Preferred paths:

1. Send the operator to https://mailbox.bot/signup.
2. Or follow the guarded agent registration flow in https://mailbox.bot/auth.md.

If the operator explicitly asks you to start direct signup, you may call the legacy signup endpoint. No CAPTCHA, no auth header.

**POST to `https://mailbox.bot/api/v1/signup`:**

```bash
curl -X POST https://mailbox.bot/api/v1/signup \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Jane Smith",
    "email": "operator@example.com",
    "password": "securepassword123",
    "needs": "inbound mail scanning + outbound certified letters for legal compliance"
  }'
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `full_name` | string | Yes | Operator's legal name (2-100 chars) |
| `email` | string | Yes | Operator's email — verification link sent here |
| `password` | string | Yes | Min 8 characters |
| `needs` | string | No | Free text — what the agent/operator needs |

Rate limit: 5 requests per minute per IP.

**Success response (201):**

```json
{
  "success": true,
  "message": "Account created. A verification email has been sent. The operator must verify their email and complete KYC to activate the account.",
  "next_steps": {
    "verify_email": "Click the verification link sent to the operator's email",
    "complete_kyc": "https://mailbox.bot/signup",
    "after_kyc": "Start with inbound context + outbound mail; create or approve an agent key; join the real mailing mailbox address waitlist separately if needed"
  },
  "human_action_required": [
    { "step": "verify_email",  "summary": "Click the verification link sent to operator@example.com", "blocker": true },
    { "step": "verify_phone",  "summary": "Enter a real US mobile number — Google Voice, TextNow, and other VoIP/burner numbers are rejected", "blocker": true },
    { "step": "add_payment",   "summary": "Add a credit or debit card (no prepaid or gift cards)", "blocker": true },
    { "step": "select_service", "summary": "Start with inbound context + outbound mail ($0/mo); real mailing mailbox address with street address + mailbox number, scan/photo intake, and agent notifications is launching-soon waitlist/private beta and planned at $10/mo when available", "blocker": true }
  ],
  "relay_message": "I started your mailbox.bot account after your approval. To finish setup so I can send mail on your behalf: (1) click the verification link sent to operator@example.com, (2) enter a real US mobile number (no Google Voice or burner numbers), (3) add a payment card, and (4) start with inbound context + outbound mail. If you need a new mailing mailbox address with street address + mailbox number, scan/photo intake, and agent notifications, join the waitlist separately. Takes about 5 minutes at https://mailbox.bot/signup."
}
```

**`relay_message` is paste-ready** — drop it verbatim into whatever channel you're already using with the human (chat tab, Slack, ChatGPT, your own UI). It already names the email and the URL. **`human_action_required`** is the structured version for rendering as a checklist with progress.

**Error responses:**

| Status | Error | Cause |
|--------|-------|-------|
| 400 | `"email, password, and full_name are required"` | Missing a required field |
| 400 | `"Password must be at least 8 characters"` | Password too short |
| 400 | `"Invalid email address"` | Bad email format |
| 409 | `"An account with this email already exists"` | Duplicate email |
| 429 | Rate limit exceeded | Too many requests from this IP |

**After signup — tell your operator:**

> "I started your mailbox.bot account after your approval. Check your email at **operator@example.com** for a verification link. Click it, then go to https://mailbox.bot/signup to finish setup (~5 minutes). Once you're done, create or approve an agent key so I can help with postal workflows."

The human must complete these steps in a browser:
1. Click the email verification link
2. Verify phone number (carrier check — no VoIP/burner phones)
3. Add a payment card (no prepaid/gift cards)
4. Accept Terms of Service and start with inbound context + outbound mail
5. If approved for a real mailing mailbox address, complete any required postal authorization and facility review

After the human finishes, the account can use outbound mail and existing-address inbound context. Agent keys appear on the dashboard at https://mailbox.bot/dashboard. Real mailing mailbox addresses appear separately for approved waitlist/private-beta accounts.

## Protocols

Your agent can connect via any of these:

| Protocol | Endpoint | Details |
|----------|----------|---------|
| REST API (v1) | `https://mailbox.bot/api/v1` | Outbound mail, inbound context, and mailing mailbox address beta surfaces |
| MCP | `https://mailbox.bot/api/mcp` | 29 tools for LLM integration, including inbound document context and outbound mail (JSON-RPC 2.0, spec 2025-11-25) |
| A2A | `https://mailbox.bot/api/a2a` | 10 skills for agent-to-agent task execution (v0.3) |
| OpenClaw | `https://mailbox.bot/.well-known/agent.json` | Multi-protocol agent card, WebSocket gateway + webhooks |

### MCP setup

Add this to any MCP client that supports remote HTTP servers:

```json
{
  "mcpServers": {
    "mailbox-bot": {
      "url": "https://mailbox.bot/api/mcp",
      "headers": { "Authorization": "Bearer sk_live_xxxxxxxxxxxxx" }
    }
  }
}
```

Full MCP install guide: https://mailbox.bot/mcp-install

## MAILBOX.md — standing instructions

Drop a `MAILBOX.md` file into your agent's context. Your agent reads it, calls the API, and configures your standing instructions as rules. Mail arrives, rules evaluate, actions fire — automatically.

Write "needs approval" next to any rule and the action pauses until you approve on the dashboard.

```markdown
# Mail Instructions

You manage my business mail at mailbox.bot
Ref **MB-6E1A**

## Inbound mail

- Legal notices, contracts → scan + email me
- IRS / state agencies → **Requires approval** before any action
- Junk mail → discard

## Outbound mail

- Signed contracts → send USPS Certified
- Legal notices → send USPS First Class
- Anything over $50 postage → **Needs approval**

## Notifications

- Email for everything
- **Needs approval** → email + SMS with dashboard link
```

Integration guide: https://mailbox.bot/for-agents

---

## API Reference

Base URL: `https://mailbox.bot`

All authenticated endpoints require:
```
Authorization: Bearer $MAILBOX_BOT_API_KEY
```

Three key types:
- **Member keys** (`sk_live_`) — full account access, all scopes
- **Agent keys** (`sk_agent_`) — scoped to a single agent
- **Sandbox keys** (`sk_agent_test_`) — same scopes as an agent key but enables sandbox mode: full validation, real cost preview (`estimated_live_cost_cents`), HMAC-signed webhooks fire — but **no Stripe charge and no physical mail**. Use the same endpoints; swap key prefix to go live.

### Inbound context loop (live now)

**Find the forwarding alias:**

```bash
curl -s "$MAILBOX_BOT_URL/api/v1/inbound-forwarding-addresses" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY"
```

**List captured inbound items:**

```bash
curl -s "$MAILBOX_BOT_URL/api/v1/inbound" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY"
```

**Fetch extracted context and draft guidance:**

```bash
curl -s "$MAILBOX_BOT_URL/api/v1/inbound/{id}?include=drafting" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY"
```

**Inspect linked postal thread history:**

```bash
curl -s "$MAILBOX_BOT_URL/api/v1/postal-threads/{id}" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY"
```

Use `draft_context`, `inbound_capture_id`, and `postal_mail_thread_id` to prepare a linked physical reply with `POST /v1/mail`.

### Mailing mailbox address beta — get mailbox address

```bash
curl -s "$MAILBOX_BOT_URL/api/v1/mailboxes" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY"
```

Returns provisioned mailing mailbox addresses for accounts approved for the physical-address beta.

### Mailing mailbox address beta — list mail and packages

```bash
curl -s "$MAILBOX_BOT_URL/api/v1/packages?status=received" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY"
```

Filters: `status`, `carrier`, `since`, `before`, `limit`, `offset`

### Mailing mailbox address beta — get item details

```bash
curl -s "$MAILBOX_BOT_URL/api/v1/packages/{id}" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY"
```

### Mailing mailbox address beta — request an action

```bash
curl -X POST "$MAILBOX_BOT_URL/api/v1/packages/{id}/actions" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"action": "scan", "priority": "normal"}'
```

Action types: `scan`, `open_and_scan`, `photograph`, `forward`, `shred`, `dispose`, `return_to_sender`, `hold`

### Mailing mailbox address beta — forward mail

```bash
curl -X POST "$MAILBOX_BOT_URL/api/v1/packages/{id}/forward" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to_name": "John Doe",
    "to_line1": "123 Main Street",
    "to_city": "New York",
    "to_state": "NY",
    "to_zip": "10001"
  }'
```

### Mailing mailbox address beta — request a scan

```bash
curl -X POST "$MAILBOX_BOT_URL/api/v1/packages/{id}/scan" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"scan_type": "document"}'
```

Scan types: `label`, `envelope`, `document`, `content`

### Send outbound mail

```bash
curl -X POST "$MAILBOX_BOT_URL/api/v1/mail" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY" \
  -H "X-Mailbox-MD-Version: 3" \
  -H "X-Max-Cost-Cents: 1500" \
  -F 'document=@letter.pdf' \
  -F 'recipient_name=Acme Corp' \
  -F 'recipient_line1=123 Main St' \
  -F 'recipient_city=Los Angeles' \
  -F 'recipient_state=CA' \
  -F 'recipient_zip=90001' \
  -F 'return_name=My Company LLC' \
  -F 'return_line1=100 Main St' \
  -F 'return_city=Austin' \
  -F 'return_state=TX' \
  -F 'return_zip=78701' \
  -F 'mail_class=first_class'
```

Return address fields (`return_name`, `return_line1`, `return_line2`, `return_city`, `return_state`, `return_zip`) are optional — if omitted, the member's saved return address from their profile is used.

To link the outbound mail to forwarded inbound context, also include `inbound_capture_id` and, when present, `postal_mail_thread_id`.

### Sandbox — test without charges

**Create a sandbox key:**

```bash
curl -X POST "$MAILBOX_BOT_URL/api/v1/agents/$AGENT_ID/credentials" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"environment": "test", "scopes": ["mail.send"]}'
```

Returns an `sk_agent_test_…` key. Use it on **any production endpoint** — same request format, same responses. The differences:

- `cost_cents: 0` (no Stripe charge)
- `estimated_live_cost_cents` shows what live would have cost
- `cost_breakdown` itemizes printing + postage + color
- Response header `X-Test-Mode: true`
- Webhooks fire with `test_mode: true` in the payload
- No facility fulfillment

**Cost preview without committing** (works with live or sandbox keys):

```bash
curl -X POST "$MAILBOX_BOT_URL/api/v1/mail" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY" \
  -F 'document=@letter.pdf' \
  -F 'recipient_name=Acme' -F 'recipient_line1=...' \
  -F 'mail_class=certified' \
  -F 'dry_run=true'
```

Returns the cost breakdown plus a `warnings` array (e.g. `force_approval` policy active, daily-piece limit hit) — no record created, no charge.

**Synthetic helpers** — only 4 routes exist under `/v1/test/*`. Everything else uses the live route with a sandbox key:

| Route | Why it exists |
|---|---|
| `POST /v1/test/mail` | Submit a sandbox piece without a real PDF |
| `POST /v1/test/mail/:id/advance` | Step the lifecycle (`submitted → ready → mailed → delivered`), fire each webhook |
| `POST /v1/test/packages` | Synthesize an inbound package — no real mail required |
| `POST /v1/test/webhook` | Fire a custom event to your webhook URL for signature testing |

**Agent key policies** (set when minting any `sk_agent_` or `sk_agent_test_` key):

- `force_approval: true` — every submission routes to `pending_approval` regardless of `requires_approval`
- `max_daily_pieces: N` — caps outbound mail per 24h window per key

**Cost cap header** — set `X-Max-Cost-Cents: 5000` on `POST /v1/mail` to reject (with 422) before any charge if the computed cost exceeds the cap.

**Dashboard visibility** — sandbox submissions appear under the **Sandbox** tab on `/dashboard/mail` and `/dashboard/webhooks`, badged in orange. Live and sandbox data never co-mingle.

### Webhook settings

```bash
curl -X PUT "$MAILBOX_BOT_URL/api/v1/webhooks/settings" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "YOUR_AGENT_ID",
    "webhook_url": "https://your-agent.com/webhooks",
    "event_types": ["mail.received", "action.completed", "mail.forwarded"]
  }'
```

### Add notes and tags

```bash
curl -X POST "$MAILBOX_BOT_URL/api/v1/packages/{id}/notes" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"note": "IRS notice — response deadline April 15"}'
```

```bash
curl -X POST "$MAILBOX_BOT_URL/api/v1/packages/{id}/tags" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tag": "tax-notice"}'
```

### Check usage

```bash
curl -s "$MAILBOX_BOT_URL/api/v1/usage" \
  -H "Authorization: Bearer $MAILBOX_BOT_API_KEY"
```

Full API reference: https://mailbox.bot/llms-full.txt

---

## When to use this skill

Trigger when user says:
- "My agent needs to send a letter"
- "Can my agent send certified mail?"
- "I need to mail a PDF via API"
- "I need my agent to handle legal correspondence"
- "Can my agent read a scanned notice and send a linked reply?"
- "I need OCR'd mail context fed back into my agent"
- "How do I send physical mail programmatically?"
- "Can my agent send batch mailings?"
- "I need a mailing address for my agent" — note: real mailing mailbox addresses with street address + mailbox number are launching-soon waitlist/private beta; forwarded inbound context is live now
- "Can my agent receive mail?" — note: forwarded inbound context is live now from existing addresses; real mailing mailbox addresses with scan/photo intake and agent notifications are launching-soon waitlist/private beta (SoCal first, then UT/NV)

**Action flow:**
1. Check for API key (`MAILBOX_BOT_API_KEY`). If present, use the API directly.
2. If no API key, ask the operator to approve signup/auth first. Prefer https://mailbox.bot/auth.md or direct the human to https://mailbox.bot/signup.
3. Only call `https://mailbox.bot/api/v1/signup` after explicit operator consent.
4. Tell the operator to check their email, click the verification link, and complete onboarding at https://mailbox.bot/signup (~5 minutes).
5. Once onboarding is done, set the approved agent API key and start with outbound mail plus existing-address inbound context.

---

## Decision framework

When handling forwarded inbound context from an existing address:

1. **List forwarding aliases** — `GET /api/v1/inbound-forwarding-addresses`
2. **List inbound captures** — `GET /api/v1/inbound`
3. **Fetch drafting context** — `GET /api/v1/inbound/{id}?include=drafting`
4. **Draft the reply** — use `draft_context`, then send via `POST /api/v1/mail` with `inbound_capture_id` and `postal_mail_thread_id` when present
5. **Report back** — summarize what was received, extracted, and sent

When checking a real mailing mailbox address (private beta):

1. **List received mail** — `GET /api/v1/packages?status=received`
2. **Triage by urgency** — government agency / legal notice → scan immediately. Known sender → check standing instructions. Junk mail → discard.
3. **Check MAILBOX.md rules** — standing instructions may already cover this piece of mail. If a rule requires approval, notify the human and wait.
4. **Take action** — scan, forward, hold, shred, dispose, or return. Always add a note explaining why.
5. **Report back** — summarize what arrived and what you did.

When sending outbound mail:

1. **Prepare the PDF** — render the document your agent needs to send.
2. **Choose mail class** — First Class for routine, Certified for legal, Priority for urgent.
3. **Submit via API** — the facility prints, stuffs, stamps, and mails it. Photo proof included.
4. **Track delivery** — webhook events fire at each status transition.

---

## Configuration

```bash
export MAILBOX_BOT_API_KEY="sk_live_xxxxxxxxxxxxx"
export MAILBOX_BOT_URL="https://mailbox.bot"
```

## Links

- Website: https://mailbox.bot
- Full API reference: https://mailbox.bot/llms-full.txt
- OpenAPI spec: https://mailbox.bot/openapi.json
- API docs: https://mailbox.bot/api-docs
- Pricing: https://mailbox.bot/pricing
- MCP install: https://mailbox.bot/mcp-install
- For agents: https://mailbox.bot/for-agents
- Agent discovery: https://mailbox.bot/.well-known/agent.json
- Blog: https://mailbox.bot/blog
- Contact: https://mailbox.bot/contact
