# Changelog

## [5.3.2] - 2026-11-10

### Changed
- FedEx prices as of 9 Nov 2026: Express Saver is $5.00 below its carrier baseline (`service_adjustment_cents: -500`), 2Day $13.00 below (`-1300`, was `-800`), Overnight $13.00 above (`1300`, was `1800`), and Ground carries a $5.00 markup (`500`)
- `delivery_signature`: optional signature on delivery for one letter (FedEx indirect $8.00, direct $8.50, adult $11.00; Priority direct $5.00, adult $11.00; Certified restricted $10.00)
- README: 55 MCP tools (was 45) and framework guide links at `/integrations/...` (the old `/docs/...` addresses redirect)

## [5.3.1] - 2026-10-11

### Changed
- Agent mailbox rental is $15/mo (was $10/mo). Mailboxes are still open to everyone and live now; allowances and usage rates are unchanged

## [5.3.0] - 2026-10-10

### Changed
- Agent mailboxes are open to everyone and **live now** at $10/mo (was $20/mo, invite only): a street address + PMB at the staffed, USPS-compliant Manhattan Beach, CA facility. The PMB number is assigned after USPS Form 1583 verification
- A mailbox is requested at signup or with `POST /v1/mailing-address-requests`, which replaces the invite request (`POST /v1/waitlist`) in the skill and README
- README adds the `npx skills add arbengine/mailbox-bot-skill` install line for Claude Code, Cursor, Codex and other agents

## [5.2.0] - 2026-09-28

### Changed
- Agent mailboxes are **Live now · invite only** since 27 Sep 2026: a street address + PMB at the staffed, USPS-compliant Manhattan Beach, CA facility ($20/mo; facility #1 holds 100 mailboxes). Removed the August 31 issuance date, the planned $10/mo price and the beta/reservation wording
- Rewrote the skill around the current physical inbound contract: `GET /v1/inbound-items?q=`, pages and quotes, `scan` / `forward` / `discard` proposals with `expected_version` and `expected_quote`, owner approval via `/decision`, webhooks `inbound.received`, `inbound.keywords_matched` and `inbound.pages_ready`, and the matching MCP tools
- Outbound guidance now sends `X-Mailbox-MD-Version`, prices First-Class from $2.00 with $0.40/page B&W and $0.70/page color, includes the FedEx 2Day and Overnight adjustments, prepaid-credit rules and queued cancellation, and the `/v1/batch-mail` flow
- MCP metadata refreshed from 30 to 45 tools to match `https://mailbox.bot/api/mcp/tools-public`; manifest logo points at the current 512px mark

## [5.1.7] - 2026-07-28

### Changed
- Corrected the published USPS one-page floors to $15.00 for Priority Mail, $20.00 for Certified Mail, and $24.00 for Certified Mail with Electronic Return Receipt
- Updated current page and color-print pricing guidance and directed agents to dry-run cost breakdowns for account-specific quotes

## [5.1.6] - 2026-07-08

### Changed
- Refreshed MCP package metadata from 29 to 30 tools to match the hosted `https://mailbox.bot/api/mcp/tools-public` catalog
- Added source-document retrieval and `document_preview_url` review flow notes for outbound mail
- Clarified that support conversations and attachments are REST/OpenAPI/dashboard features, not MCP tools

## [5.1.5] - 2026-06-05

### Changed
- Made the launching-soon real mailing address beta more explicit across skill metadata: street address + mailbox number, scan/photo intake, OCR/classification, agent notifications, and linked reply workflows
- Replaced generic managed-address phrasing in discovery copy with user-facing waitlist language

## [5.1.4] - 2026-06-05

### Changed
- Quoted and shortened the ClawHub frontmatter description so the registry can derive the public summary from the current package copy

## [5.1.3] - 2026-06-05

### Changed
- Removed technical mailbox-provider jargon from public skill copy
- Reframed waitlist language around a real mailing mailbox address with street address + mailbox number
- Reconfirmed live capabilities and pricing language for ClawHub/OpenClaw readers

## [5.1.2] - 2026-06-05

### Changed
- Refreshed ClawHub package version metadata

## [5.1.1] - 2026-06-05

### Changed
- Fixed stale ClawHub-facing pricing and onboarding language in `SKILL.md`
- Clarified that direct signup requires explicit operator consent and that `auth.md` is the preferred guarded registration path
- Updated OpenClaw install and ClawHub publish instructions for the v5.1.1 package

## [5.1.0] - 2026-05-27

### Changed
- Reframed the skill around two live workflows: outbound physical mail and forwarded inbound document context
- Updated README and SKILL.md to distinguish live inbound context from the mailing mailbox address private beta
- Fixed MCP install docs to use current tool names such as `list_inbound_forwarding_addresses`, `list_inbound_mail`, and `get_inbound_mail`
- Updated outbound examples to `X-Mailbox-MD-Version: 3` and canonical OpenAPI links to `https://mailbox.bot/openapi.json`
- Refreshed marketplace metadata descriptions and tags to mention inbound context and postal threads

## [5.0.0] - 2026-05-01

### Changed
- Repositioned to outbound-first: "The physical mail API for AI agents and software workflows"
- Updated README with badges, install-first layout, and sandbox documentation
- Updated SKILL.md frontmatter with new tags and description
- Inbound mailbox status clarified as "controlled private beta" (not "coming soon")

### Added
- `llms-install.md` — install guide for Cline, Cursor, Claude Code
- `server.json` — standardized MCP server metadata for directory submissions
- `smithery.yaml` — Smithery marketplace metadata
- `CHANGELOG.md` — this file
- Sandbox documentation (test keys, dry runs, lifecycle simulation)
- Billing safeguards documentation (X-Max-Cost-Cents, dry_run, spend caps)

## [4.0.0] - 2026-04-15

### Added
- SKILL.md with full API reference, decision framework, and configuration
- Outbound mail: send letters, certified mail, batch mailings via API
- MAILBOX.md standing instructions with human-in-the-loop approval gates
- MCP (29 tools), A2A, OpenClaw, REST protocols
- Webhook notifications with HMAC-SHA256 signing
- Multi-channel notifications: email, SMS, Slack, Discord

### Changed
- README updated with ClawHub publishing instructions

## [3.0.0] - 2026-03-20

### Added
- Initial OpenClaw skill with inbound package management
- Action system: scan, forward, shred, hold, dispose, return
- Agent rules and expected shipment matching
- Package tagging and notes
