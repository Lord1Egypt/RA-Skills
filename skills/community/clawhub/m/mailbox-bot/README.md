# mailbox.bot — Postal Mail API and MCP Server for AI Agents

[![Website](https://img.shields.io/badge/Website-mailbox.bot-1D4ED8?style=flat)](https://mailbox.bot)
[![API Docs](https://img.shields.io/badge/API_Docs-api--docs-1D4ED8?style=flat)](https://mailbox.bot/api-docs)
[![MCP](https://img.shields.io/badge/MCP-29_tools-1D4ED8?style=flat)](https://mailbox.bot/mcp-install)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-1D4ED8?style=flat)](https://mailbox.bot/openapi.json)
[![Sandbox](https://img.shields.io/badge/Sandbox-test_keys-1D4ED8?style=flat)](https://mailbox.bot/api-docs#sandbox)
[![License](https://img.shields.io/badge/License-Proprietary-gray?style=flat)]()
[![Status](https://img.shields.io/badge/Status-Two_Workflows_Live-34d399?style=flat)]()
[![smithery badge](https://smithery.ai/badge/reportinganddata/mailbox-bot)](https://smithery.ai/servers/reportinganddata/mailbox-bot)

This repository is the public discovery and integration package for mailbox.bot. The production service runs at [mailbox.bot](https://mailbox.bot).

**Two live workflows today: outbound physical mail via API, and inbound forwarded document context for reply loops. If an operator wants a new real mailing mailbox address with street address + mailbox number for an AI agent, use the launching-soon waitlist/private beta; do not describe new receiving addresses as generally available.**

mailbox.bot is the postal mail API for AI agents and software workflows. Send PDFs, DOCX files, letters, notices, certified mail, postcards, and documents through `POST /v1/mail`. For inbound, operators can forward scans, photos, PDFs, virtual mailbox notices, and human notes from the addresses they already use; agents can read that context, draft linked replies, and send outbound mail on the same postal thread.

```text
forward scans/docs -> OCR-backed context + draft reply -> POST /v1/mail
```

## Two live workflows

1. **Outbound physical mail API** — submit a document and recipient address with `POST /v1/mail`.
2. **Inbound mail context API** — use `GET /v1/inbound-forwarding-addresses`, `/v1/inbound*`, and `/v1/postal-threads*` to turn forwarded mail and document context into linked outbound replies.

Default inbound forwarding is a digital intake channel, not a newly assigned physical mailing address. Real mailing mailbox addresses remain a separate launching-soon waitlist/private-beta surface with scan/photo intake and agent notifications.

## Install

### MCP server

Add to your MCP config:

```json
{
  "mcpServers": {
    "mailbox-bot": {
      "url": "https://mailbox.bot/api/mcp",
      "headers": { "Authorization": "Bearer sk_agent_..." }
    }
  }
}
```

Full MCP install guide: [mailbox.bot/mcp-install](https://mailbox.bot/mcp-install)

### OpenClaw

```bash
clawhub install mailbox-bot
# or in OpenClaw:
openclaw skills install arbengine/mailbox-bot
```

### REST API

```bash
curl -X POST https://mailbox.bot/api/v1/mail \
  -H "Authorization: Bearer sk_agent_..." \
  -H "X-Mailbox-MD-Version: 3" \
  -H "X-Max-Cost-Cents: 1500" \
  -F 'document=@letter.pdf' \
  -F 'recipient_name=Acme Corp' \
  -F 'recipient_line1=123 Main St' \
  -F 'recipient_city=Los Angeles' \
  -F 'recipient_state=CA' \
  -F 'recipient_zip=90001' \
  -F 'mail_class=certified' \
  -F 'dry_run=true'
```

## What's live now

- **Outbound mail** — submit a PDF, facility prints, stuffs, stamps, and mails it with photo proof
- **Inbound document context** — private forwarding aliases on `forward.mailbox.bot` capture scans, photos, PDFs, provider notices, and human notes from the addresses operators already use
- **OCR-backed reply loop** — agents read `/v1/inbound*`, retrieve `draft_context`, and send linked replies with `inbound_capture_id` and `postal_mail_thread_id`
- **Postal threads** — `/v1/postal-threads*` ties inbound context and outbound events together
- **Certified mail** — USPS Certified, Certified + Return Receipt, Priority, First Class
- **FedEx and UPS** — zone-based rates for overnight, 2-day, ground
- **Batch mail** — send up to 10,000 pieces from a CSV, volume discounts at 500/1000/5000 pieces
- **Sandbox** — test keys (`sk_agent_test_`), dry runs, lifecycle simulation, zero charges
- **Webhook notifications** — HMAC-signed JSON payloads fire on every status transition
- **MAILBOX.md standing instructions** — configure rules for outbound mail and future mailing mailbox workflows
- **Human-in-the-loop** — `requires_approval=true` pauses for human approval
- **Billing safeguards** — `X-Max-Cost-Cents` header, `dry_run=true`, daily spend caps

## Waitlist — real mailing mailbox address

A real mailing mailbox address for your agent is a launching-soon waitlist/private beta unless the account is explicitly approved. This is separate from the live forwarded inbound context flow. Activation will require identity verification, any required postal authorization, and facility approval.

- Street address + mailbox number for approved accounts
- Arrival photos, requested/instructed scans, OCR, and classification
- Agent pings through MCP/API/webhooks so workflows can triage, decide, and send linked replies at scale
- Actions via API: scan, forward, hold, shred, dispose, return to sender
- Agent memory: tag and annotate mail with persistent notes and metadata

## Protocols

| Protocol | Endpoint | Details |
|----------|----------|---------|
| REST API | `https://mailbox.bot/api/v1` | Outbound mail, inbound forwarding context, and launching-soon mailing address beta actions |
| MCP | `https://mailbox.bot/api/mcp` | 29 tools for outbound mail, inbound context, and launching-soon mailing address beta actions |
| A2A | `https://mailbox.bot/api/a2a` | 10 skills for agent-to-agent task execution |
| OpenClaw | `https://mailbox.bot/.well-known/agent.json` | Multi-protocol agent card |

## Plans

| Plan | Price | Status | What you get |
|------|-------|--------|-------------|
| **Inbound context + outbound mail** | $0/mo | **Live now** | Private inbound forwarding alias included. Send outbound mail by dashboard, API, or MCP. |
| **Real mailing mailbox address** | Planned $10/mo | **Launching-soon waitlist/private beta** | Street address + mailbox number for approved users only, with scan/photo intake and agent notifications. Separate from forwarded inbound context. |

Outbound pricing: First Class starts at $1.00 for a 1-page letter, then +$0.40 per extra page. USPS 1-page pricing: Priority Flat Rate Envelope $14.85, Certified Mail $8.98, Certified + Return Receipt $13.38. Color printing +$0.25/page. FedEx and UPS envelope rates are zone-based and shown at checkout.

Full pricing: [mailbox.bot/pricing](https://mailbox.bot/pricing)

## Framework integrations

No SDK required — all integrations use the REST API via standard HTTP libraries.

- [LangChain](https://mailbox.bot/docs/langchain) (Python)
- [CrewAI](https://mailbox.bot/docs/crewai) (Python)
- [LlamaIndex](https://mailbox.bot/docs/llamaindex) (Python)
- [Vercel AI SDK](https://mailbox.bot/docs/vercel-ai-sdk) (TypeScript)
- [OpenAI Agents SDK](https://mailbox.bot/docs/openai-agents-sdk) (Python)

## Links

- [Website](https://mailbox.bot)
- [API Docs](https://mailbox.bot/api-docs)
- [Full API Reference (LLM-friendly)](https://mailbox.bot/llms-full.txt)
- [MCP Install Guide](https://mailbox.bot/mcp-install)
- [MCP Server Card](https://mailbox.bot/.well-known/mcp/server-card.json)
- [Public MCP Tool Catalog](https://mailbox.bot/api/mcp/tools-public)
- [Official MCP Registry Name](https://registry.modelcontextprotocol.io) — `bot.mailbox/mailbox`
- [Sandbox & Test Keys](https://mailbox.bot/api-docs#sandbox)
- [OpenAPI Spec](https://mailbox.bot/openapi.json)
- [Agent Discovery](https://mailbox.bot/.well-known/agent.json)
- [Pricing](https://mailbox.bot/pricing)
- [Contact](https://mailbox.bot/contact)

## Publishing to ClawHub (for maintainers)

```bash
npm install -g clawhub
clawhub login
clawhub publish . \
  --slug mailbox-bot \
  --name "mailbox.bot" \
  --version 5.1.5 \
  --changelog "v5.1.5 — makes the launching-soon real mailing address beta explicit: street address + mailbox number, scan/photo intake, OCR/classification, agent notifications, and linked reply workflows."
clawhub inspect mailbox-bot
```

---

Questions? [mailbox.bot/contact](https://mailbox.bot/contact)
