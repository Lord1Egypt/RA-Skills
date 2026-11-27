---
name: mapbulk
description: Use the MapBulk MCP server to find local businesses from Google Maps, add the emails they publish on their own websites plus website context, inspect saved leads, and export CSV, JSON or XLSX. Use it when the user wants a business lead list for a city, niche or country, or wants to work with their existing MapBulk lists and credits.
---

# MapBulk

MapBulk is a Google Maps lead scraper that adds the emails businesses publish on their own websites, plus website context, for cold outreach.

## Connect

- Remote MCP server: `https://api.mapbulk.com/mcp` (Streamable HTTP).
- In Claude and ChatGPT connectors, the user signs in to MapBulk with OAuth. Any MapBulk account works and no paid plan is needed; new accounts start with welcome credits.
- In local agents (Claude Code, Codex, Gemini CLI, OpenClaw, Hermes and others), send `Authorization: Bearer <MAPBULK_API_KEY>`. API keys are created at https://app.mapbulk.com under "API, MCP & CLI" and need the Scale or Max plan. Keep the key in the client's secret storage, never in prompts, URLs or logs.
- Details: https://mapbulk.com/auth.md and https://mapbulk.com/docs/?article=mcp

## Tools

Run `tools/list` for the current input schemas.

| Tool | Purpose |
| --- | --- |
| `list_business_categories` | Search or browse the versioned category catalog |
| `search_businesses` | Create one saved list (campaign) with an approved target and credit limit |
| `list_searches` | List the account's saved lists, newest first |
| `get_search_job` | Read a list's status, progress and stop reason |
| `get_search_results` | Read one page of a list's results, optionally only those with an email |
| `list_leads` | Read one page of saved leads across lists |
| `get_search_issues` | Read stored issues for a list |
| `get_usage` | Read the credit balance and usage |
| `enrich_businesses` | Find published emails for an existing list or imported websites |
| `cancel_search` | Stop a running list and keep what was collected |
| `retry_search` | Retry eligible failed work in a list |
| `export_results` | Create CSV, JSON or XLSX exports of a finished list |
| `get_export` | Read an export's status, format, size and expiry |
| `download_export` | Return a ready CSV or JSON export's content, up to 1 MB |

## Credits and approval

- A business costs 0.5 credit; each accepted email found on its website adds 0.5 credit. Website context comes with the email. You pay only for what is delivered.
- Tool inputs count half-credit units: 2 units = 1 credit.
- Read tools cost nothing. Before any tool that can spend credits (`search_businesses`, `enrich_businesses`, `retry_search`), confirm the business type, location, number of businesses and the maximum credits with the user.
- For a finite search set `result_cap` and `maximum_credit_units`. Never use `result_mode: "all"` unless the user explicitly asks to use their whole balance.
- Give each write a unique `idempotency_key` and reuse it with the same inputs after a timeout; don't start a replacement list to recover an uncertain request. A `409` means: check the list's state, don't retry blindly.

## Categories and results

- Search `list_business_categories` and keep the returned catalog version with the selected node IDs in `category_selection`. Browse nodes are navigation, not selectable categories.
- Follow `get_search_job` until the list is finished; page results with the returned cursor. Keep the user's "with email only" choice the same for results and exports.
- Report partial or failed lists honestly. Every email domain is checked for a mail server (MX); that is not mailbox verification, and a published email is not marketing consent. MapBulk does not send emails.

## Exports

1. `export_results` with the list ID and formats (`csv`, `json`, `xlsx`).
2. `get_export` until the export is ready.
3. `download_export` returns CSV or JSON content up to 1 MB. Larger files and XLSX are downloaded from the MapBulk dashboard. Download links are private; don't share them.

## Example

After the user approves 10 dentists in Austin with at most 10 credits:

```json
{"query":"dentist","country_code":"US","locations":["Austin, TX"],"result_cap":10,"maximum_credit_units":20,"enrichment":true,"idempotency_key":"user-approved-search-001"}
```

Support: https://mapbulk.com/contact · Privacy: https://mapbulk.com/privacy-policy · Terms: https://mapbulk.com/terms-of-service
