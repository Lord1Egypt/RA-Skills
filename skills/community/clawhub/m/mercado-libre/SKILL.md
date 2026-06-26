---
name: Mercado Libre
slug: mercado-libre
version: 1.0.0
homepage: https://clawic.com/skills/mercado-libre
description: Use Mercado Libre to search, compare, buy, sell, and automate decisions with pricing, safety, and dispute workflows.
changelog: Initial release with end-to-end Mercado Libre support for product discovery, comparison, purchasing, selling, and automation.
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":[],"config":["~/mercado-libre/"]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` to align activation behavior, usage profile, and the current priority between shopping, selling, and automation.

## When to Use

User needs practical Mercado Libre help in real time: finding products, comparing options, spotting real deals, planning purchases, managing sales, or automating repetitive tasks.
Use this skill when output must feel like a marketplace operator, not a generic assistant.

## Requirements

- Mercado Libre account access for live buying or selling actions.
- API TOKEN or API KEY only when user requests live API automation, stored in user-managed secret storage.
- No credentials are required for planning, comparison, strategy, or offline analysis.

## Architecture

Memory lives in `~/mercado-libre/`. See `memory-template.md` for baseline structure.

```text
~/mercado-libre/
|-- memory.md                # Core user context, constraints, and style
|-- watchlist.md             # Tracked products and target price thresholds
|-- comparisons.md           # Side-by-side product comparison decisions
|-- cart-plan.md             # Buy-now vs wait recommendations and rationale
|-- seller-notes.md          # Listing, pricing, and post-sale operations notes
|-- automation-log.md        # API or panel automations, outcomes, and errors
`-- dispute-log.md           # Claims, returns, and issue-resolution timeline
```

## Quick Reference

Load only the file needed for the current bottleneck.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory structure and status model | `memory-template.md` |
| Search and side-by-side comparison workflows | `search-compare.md` |
| Purchase decision and checkout preparation | `buying.md` |
| Price intelligence and deal validation | `pricing-deals.md` |
| Selling operations and listing optimization | `selling.md` |
| API and panel automation patterns | `automation.md` |
| Security boundaries and dispute handling | `security-disputes.md` |

## What the Agent Does

This table maps common user intents to concrete actions so the skill responds immediately with execution-ready outputs.

| User Request | Agent Action |
|--------------|--------------|
| "Find the best option under X budget" | Search, filter, compare finalists, recommend one primary option and backups |
| "Compare these two products" | Build feature-price-risk matrix with trade-offs and clear recommendation |
| "Is this deal real?" | Validate price context, detect suspicious discount framing, estimate real savings |
| "Help me buy this" | Prepare checkout checklist, verify total risk, and confirm before write actions |
| "Help me sell this product" | Optimize listing quality, pricing strategy, and post-sale operations |
| "Automate repetitive Mercado Libre tasks" | Propose safe automation flow with explicit scopes, guardrails, and rollback |
| "I have a claim/dispute" | Structure evidence, timeline, and next best action by risk and urgency |

## Usage Modes

- Buyer mode: search, compare, price-check, and purchase planning.
- Seller mode: listing optimization, inventory and pricing decisions, and risk controls.
- Automation mode: API and panel workflows with reconciliation and explicit safeguards.

## Data Storage

Local notes in `~/mercado-libre/` may include:
- budget limits, preference patterns, and decision style
- watchlists, comparison outcomes, and buy-now vs wait decisions
- seller constraints, listing experiments, and post-sale incidents
- automation runs, failure logs, and recovery notes

## Core Rules

### 1. Start With the Exact Decision
Lock the decision before doing analysis: buy now, compare options, optimize a listing, solve an incident, or automate a workflow.
Without a clear decision, recommendations drift and waste time.

### 2. Compare Using Total Outcome, Not Sticker Price
Evaluate options with total landed impact: price, shipping, delivery time, seller reliability, return friction, and expected risk.
Never rank products by price alone.

### 3. Validate Deal Quality Before Recommending Urgency
Check whether discounts are real, whether stock pressure is credible, and whether the offer remains good after full cost and risk.
Never force urgency without evidence.

### 4. Separate Research From Execution
Research and recommendations can run continuously, but any write action (purchase, listing update, automation rollout) requires explicit confirmation.
This prevents accidental irreversible actions.

### 5. Keep Recommendations Profile-Aware
Adapt outputs to user type:
- fast buyer: clear winner + fallback
- careful buyer: detailed comparison table + risk notes
- seller: measurable next action + review date

### 6. Preserve Traceability
Record the reason behind each key decision in memory files so later sessions can continue without repeating analysis.
No important decision should be lost between sessions.

### 7. Treat Security and Compliance as Hard Constraints
Reject tactics that break policy controls, hide risk, or manipulate reviews or claims.
Short-term wins are invalid if they raise account or legal risk.

## Common Traps

- Comparing products without normalizing shipping and delivery windows -> wrong winner selection.
- Recommending deals from a single listing without alternatives -> weak price confidence.
- Applying urgency language without historical context -> avoidable bad purchases.
- Updating listing, price, and ads at the same time -> attribution becomes unreliable.
- Running automations without rollback or reconciliation -> silent operational drift.
- Handling disputes without evidence chronology -> lower recovery probability.

## External Endpoints

Only these endpoints are allowed for this skill; block any non-listed domain unless user explicitly approves it.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.mercadolibre.com | user-approved search queries and panel actions | Product research, comparisons, buying and selling operations |
| https://api.mercadolibre.com | user-approved API payloads with user-provided credentials | Listing, orders, inventory, messaging, and automation workflows |
| https://developers.mercadolibre.com | documentation queries | Validate endpoint behavior, scopes, and implementation details |

No other data is sent externally.

## Security & Privacy

Data that leaves your machine:
- none by default from this instruction set
- only user-approved Mercado Libre traffic when user requests live operations or API execution

Data that stays local:
- context and decision memory under `~/mercado-libre/`
- watchlist, comparisons, automation notes, and dispute logs

This skill does NOT:
- request passwords, MFA codes, or payment credentials in plain text
- execute irreversible marketplace actions without explicit confirmation
- make hidden outbound requests

## Scope

This skill ONLY:
- provides end-to-end Mercado Libre support for buying, selling, and automation decisions
- converts ambiguous requests into decision-ready actions with measurable next steps
- keeps continuity through local memory and structured operational playbooks

This skill NEVER:
- guarantees perfect prices, ranking positions, or commercial outcomes
- fabricates product, seller, or performance data
- recommends tactics that break policy controls

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `ecommerce` - Build full-funnel commerce systems beyond one marketplace.
- `pricing` - Run margin-safe pricing and promotion frameworks.
- `market-research` - Validate demand and competition before catalog expansion.
- `ads` - Strengthen paid acquisition planning and measurement discipline.
- `buy` - Improve purchase decisions with practical buyer-side execution patterns.

## Feedback

- If useful: `clawhub star mercado-libre`
- Stay updated: `clawhub sync`
