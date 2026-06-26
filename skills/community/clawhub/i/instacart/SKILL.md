---
name: Instacart
slug: instacart
version: 1.0.0
homepage: https://clawic.com/skills/instacart
description: Build Instacart recipe pages, shopping lists, and retailer lookups with MCP, REST, secure auth, and launch-ready integration rules.
changelog: Initial release with MCP, REST, Connect boundary, and API integration playbooks for Instacart.
metadata: {"clawdbot":{"emoji":"IC","requires":{"env":["INSTACART_API_KEY"],"bins":["jq"]},"primaryEnv":"INSTACART_API_KEY","os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` for integration guidelines.

## When to Use

User needs Instacart-specific execution rather than generic grocery advice. Activate for shoppable recipe pages, shopping list pages, nearby retailer lookup, MCP-based agent handoff, launch-readiness checks, or API troubleshooting around Instacart Developer Platform.

## Architecture

Memory lives in `~/instacart/`. See `memory-template.md` for setup.

```text
~/instacart/
|-- memory.md                # Operating context, activation rules, approved surfaces
|-- url-cache.md             # Payload hashes and generated products_link URLs
|-- retailer-notes.md        # Preferred retailers, geo defaults, and known-good keys
|-- launch-notes.md          # Production approval state and messaging constraints
`-- incidents.md             # Failed requests, root causes, and fixes
```

## Quick Reference

Use the smallest relevant file for the current task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory schema and status values | `memory-template.md` |
| Auth, environments, and key model | `auth-playbook.md` |
| Core endpoint coverage | `endpoint-map.md` |
| Request bodies, payload shaping, and curl examples | `request-patterns.md` |
| MCP server setup and tool limits | `mcp-integration.md` |
| Connect and fulfillment boundaries | `connect-boundaries.md` |
| Errors, retries, and low-signal matches | `troubleshooting.md` |

## Requirements

- Required secret: `INSTACART_API_KEY`
- Required tool for the documented smoke tests: `jq`
- Optional tool for MCP Inspector workflows: `npx`
- Optional: MCP Inspector for validating MCP connectivity

Never ask the user to paste API keys into chat. Use environment variables or their existing secret manager.

## Data Storage

Local notes in `~/instacart/` should store:
- approved environment and surface selection
- geo defaults such as `country_code` and common postal codes
- known-good payload shapes and normalized line-item conventions
- generated link cache keyed by normalized content hash
- production approval status and messaging restrictions

## Core Rules

### 1. Choose the Right Surface Before Sending Traffic
Decide explicitly between:
- Developer Platform MCP for agent-native `create-recipe` and `create-shopping-list`
- Developer Platform REST for recipe pages, shopping list pages, and nearby retailers with full request control
- Instacart Connect for branded ecommerce, fulfillment, post-checkout, sandbox callbacks, or retailer workflows

Do not mix these surfaces casually. Wrong routing creates auth failures, wrong expectations, and rework.

### 2. Lock Environment, Auth, and Scope First
Before any request, confirm:
- development or production
- the correct base URL for that environment
- `Authorization: Bearer <API key>` for Developer Platform REST
- whether the API key has the required permission level and endpoint access

Production keys should only be used after the integration has passed Instacart review and is active.

### 3. Normalize Inputs for Matching, Not Human Prose
Instacart matching is heuristic. For each ingredient or line item:
- keep `name` generic and searchable
- keep brand preferences in `filters.brand_filters`
- keep health preferences in `filters.health_filters`
- use either `product_ids` or `upcs`, never both
- use supported units and positive quantities only

Do not hide size, brand, dietary intent, and geo assumptions inside one noisy string.

### 4. Validate Geo and Retailer Context Up Front
For nearby retailer lookup, use `postal_code` plus `country_code`.
- current public docs show `US` and `CA`
- retailer lookup returns organization-level `retailer_key`, not a specific store id
- a valid postal code does not guarantee good ingredient coverage

Run retailer lookup before presenting a user-facing link when store relevance matters.

### 5. Add Client-Side Idempotency
Recipe and shopping-list creation return a fresh `products_link_url`, and the docs recommend caching until content changes.
- canonicalize the request payload
- hash the normalized payload plus environment
- reuse the stored URL when nothing material changed
- regenerate only when title, items, instructions, filters, or link settings changed

Do not spam page-creation endpoints for equivalent content.

### 6. Treat Measurements and Filters as Ranking Inputs
Ordering and correctness matter:
- for countable items, prefer `each`
- if multiple measurements are provided, order them intentionally
- keep brand and health filters separate from the product name
- keep brand spelling and health filters exact
- stay conservative on filter count per item for better matches

Poor units and noisy names are a common cause of missing quantity or weak matches.

### 7. Respect Launch and Messaging Constraints
Before moving to production:
- complete development testing
- pass the pre-launch and approval workflow
- assume a new production key is non-functional while pending approval
- keep public messaging and logo usage aligned with Instacart guidelines

Never claim Instacart endorsement, invent brand usage rules, or ship production messaging without checking current guidance.

## Common Traps

- Using Connect when the task only needs a shoppable page -> heavier auth and wrong integration surface
- Using MCP for retailer lookup -> current MCP toolset does not cover it
- Mixing `product_ids` and `upcs` on the same item -> 400 validation error
- Repeating the same UPC or product id across multiple items -> duplicate identifier errors
- Stuffing brands into `name` instead of `brand_filters` -> weaker fallback matching
- Sending unsupported or vague units -> product may match without a useful quantity
- Treating `retailer_key` as a specific store record -> bad downstream assumptions
- Recreating identical pages on every run -> unnecessary link churn and harder attribution
- Requesting production traffic before approval -> key stays pending and does not function
- Publishing UI or marketing copy without guideline review -> launch risk and brand rejection

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://connect.dev.instacart.tools | API key header, retailer lookup params, page-creation payloads | Developer Platform development REST traffic |
| https://connect.instacart.com | API key header, retailer lookup params, page-creation payloads | Developer Platform production REST traffic |
| https://mcp.dev.instacart.tools/mcp | API key header and tool payloads | Development MCP server for agent testing |
| https://mcp.instacart.com/mcp | API key header and tool payloads | Production MCP server |
| https://dashboard.instacart.com | Account and API key management traffic | Create keys and review approval state |
| https://enterprise-servicedesk.instacart.com | Support case metadata | Escalate rejected or broken integrations |

No other data should be sent externally unless the user explicitly adopts Instacart Connect or additional partner programs.

## Security & Privacy

Data that leaves your machine:
- request bodies for recipe pages and shopping list pages
- retailer lookup parameters such as postal code and country
- API key authentication headers
- optional MCP tool payloads

Data that stays local:
- caches and operating notes in `~/instacart/`
- request diffs, retry notes, and approved retailer defaults
- raw secrets if the user stores them in an environment manager

This skill does NOT:
- request API keys in chat
- bypass Instacart approval gates
- imply retailer fulfillment features are available through Developer Platform page APIs
- send undeclared traffic outside the documented Instacart surfaces

## Trust

By using this skill, data is sent to Instacart services and any explicitly configured Connect workflows.
Only install and run it if you trust Instacart with the grocery and integration data you send.

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `api` - Build reliable REST request and error-handling patterns
- `auth` - Structure credential hygiene and environment separation
- `grocery` - Handle grocery-domain planning and item taxonomy
- `webhook` - Model callback verification and event-driven workflows
- `workflow` - Turn repeated integration steps into clear operating runbooks

## Feedback

- If useful: `clawhub star instacart`
- Stay updated: `clawhub sync`
