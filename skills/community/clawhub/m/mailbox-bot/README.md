# mailbox.bot — Postal Mail API and MCP Server for AI Agents

[![Website](https://img.shields.io/badge/Website-mailbox.bot-1D4ED8?style=flat)](https://mailbox.bot)
[![API Docs](https://img.shields.io/badge/API_Docs-api--docs-1D4ED8?style=flat)](https://mailbox.bot/api-docs)
[![MCP](https://img.shields.io/badge/MCP-45_tools-1D4ED8?style=flat)](https://mailbox.bot/mcp-install)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-1D4ED8?style=flat)](https://mailbox.bot/openapi.json)
[![Sandbox](https://img.shields.io/badge/Sandbox-test_keys-1D4ED8?style=flat)](https://mailbox.bot/api-docs#sandbox)
[![License](https://img.shields.io/badge/License-Proprietary-gray?style=flat)]()
[![Status](https://img.shields.io/badge/Status-Live_now-34d399?style=flat)]()
[![smithery badge](https://smithery.ai/badge/reportinganddata/mailbox-bot)](https://smithery.ai/servers/reportinganddata/mailbox-bot)

This repository is the public discovery and integration package for mailbox.bot. The production service runs at [mailbox.bot](https://mailbox.bot).

**MCP server lets AI agents send physical mail.**

**Live now: outbound physical mail via API and MCP, forwarded document context, and agent mailboxes: a street address + PMB at the staffed, USPS-compliant Manhattan Beach, CA facility for $15/mo. Get one at signup or with `POST /v1/mailing-address-requests`. The PMB number is assigned after USPS Form 1583 verification.**

mailbox.bot is the postal mail API for AI agents and software workflows. Send PDFs, DOCX files, letters, notices, certified mail, postcards, and documents through `POST /v1/mail`. For inbound, operators can forward scans, photos, PDFs, virtual mailbox notices, and human notes from the addresses they already use; agents can read that context, draft linked replies, and send outbound mail on the same postal thread.

```text
forward scans/docs -> OCR-backed context + draft reply -> POST /v1/mail
```

## What agents can do

1. **Outbound physical mail API** — submit a document and recipient address with `POST /v1/mail`.
2. **Agent mailbox** — search mail at the assigned address with `GET /v1/inbound-items?q=`, read OCR pages, and propose `scan`, `forward` or `discard` with `POST /v1/inbound-items/{id}/actions`; the owner approves each proposal at the quoted price.
3. **Inbound mail context API** — use `GET /v1/inbound-forwarding-addresses`, `/v1/inbound*`, and `/v1/postal-threads*` to turn forwarded mail and document context into linked outbound replies.

Default inbound forwarding is a digital intake channel, not a physical address. The agent mailbox is the physical receiving product: staff log each letter and package, OCR scanned pages, and carry out the action an agent proposes once its human approves.

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

### Claude Code, Cursor, Codex and other agents

```bash
npx skills add arbengine/mailbox-bot-skill
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
- **Document review** — `requires_approval=true` creates dashboard review items with `document_preview_url`
- **Certified mail** — USPS Certified, Certified + Return Receipt, Priority, First Class
- **FedEx and UPS** — zone-based rates for overnight, 2-day, ground
- **Batch mail** — one PDF plus one CSV through `/v1/batch-mail` (estimate, draft, confirm), with a sandbox
- **Sandbox** — test keys (`sk_agent_test_`), dry runs, lifecycle simulation, zero charges
- **Webhook notifications** — HMAC-signed JSON payloads fire on every status transition
- **MAILBOX.md standing instructions** — configure rules for outbound mail and agent mailbox workflows
- **Human-in-the-loop** — `requires_approval=true` pauses for human approval
- **Billing safeguards** — `X-Max-Cost-Cents` header, `dry_run=true`, daily spend caps

## Agent mailbox — Live now

A real street address + PMB for your agent at the staffed, USPS-compliant Manhattan Beach, CA facility, $15/mo. Mailboxes are live now: get one at signup or with `POST /v1/mailing-address-requests`. The PMB number is assigned after USPS Form 1583 verification. USPS Form 1583 ties a verified human to every agent mailbox: one online notary session, two IDs, fee waived.

- **Arrives** — staff log each letter and package with an envelope photo; webhooks `inbound.received`, `inbound.keywords_matched` and `inbound.pages_ready`
- **Reads** — `GET /v1/inbound-items?q=` searches senders, references and OCR text; `GET /v1/inbound-items/{id}/pages` returns OCR per page
- **Acts** — `POST /v1/inbound-items/{id}/actions` proposes `scan`, `forward` or `discard`; the owner approves at the quoted price
- **Plan** — $15/mo includes 30 pieces and 5 packages a month and two Open & scan requests; `GET /v1/inbound-plan` returns every rate
- **Sandbox** — `sk_agent_test_` keys use the same routes on the account's sample letter, with nothing charged

No mailbox yet? Request a mailing address # with `POST /v1/mailing-address-requests`; the human finishes USPS Form 1583 online.

## Protocols

| Protocol | Endpoint | Details |
|----------|----------|---------|
| REST API | `https://mailbox.bot/api/v1` | Outbound mail, agent mailbox reads and actions, and inbound forwarding context |
| MCP | `https://mailbox.bot/api/mcp` | 55 tools for outbound mail, agent mailbox search and actions, inbound context, facility messaging, webhooks, and sandbox lifecycle simulation |
| A2A | `https://mailbox.bot/api/a2a` | 10 skills for agent-to-agent task execution |
| OpenClaw | `https://mailbox.bot/.well-known/agent.json` | Multi-protocol agent card |

## Plans

| Plan | Price | Status | What you get |
|------|-------|--------|-------------|
| **Inbound context + outbound mail** | $0/mo | **Live now** | Private inbound forwarding alias included. Send outbound mail by dashboard, API, or MCP. |
| **Agent mailbox** | $15/mo | **Live now** | Street address + PMB at the Manhattan Beach, CA facility; 30 pieces and 5 packages a month included; scan, forward or discard with owner approval. |

Outbound pricing: a 1-page USPS First-Class letter starts at $2.00; printing is $0.40/page B&W or $0.70/page color total (including the $0.30/page color upgrade). Published USPS 1-page floors are Priority Mail $15.00, Certified Mail $20.00, and Certified + Electronic Return Receipt $24.00. FedEx 2Day takes a fixed $8.00 reduction and FedEx Overnight a fixed $18.00 adjustment after the carrier baseline. Outbound mail uses prepaid credits; use `dry_run=true` and `cost_breakdown` for the authoritative quote.

Full pricing: [mailbox.bot/pricing](https://mailbox.bot/pricing)

## Framework integrations

No SDK required — all integrations use the REST API via standard HTTP libraries.

- [LangChain](https://mailbox.bot/integrations/langchain) (Python)
- [CrewAI](https://mailbox.bot/integrations/crewai) (Python)
- [LlamaIndex](https://mailbox.bot/integrations/llamaindex) (Python)
- [Vercel AI SDK](https://mailbox.bot/integrations/vercel-ai-sdk) (TypeScript)
- [OpenAI Agents SDK](https://mailbox.bot/integrations/openai-agents-sdk) (Python)

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
  --version 5.3.2 \
  --changelog 'v5.3.2 — FedEx prices from 9 Nov 2026 (Express Saver, 2Day and Overnight $5.00 lower, Ground +$5.00), signature on delivery, 55 MCP tools and current guide links.'
clawhub inspect mailbox-bot
```

---

Questions? [mailbox.bot/contact](https://mailbox.bot/contact)
