---
name: nexez-agent-discovery
description: Discover Nexez agent pages, compare AI-ready offers, and safely hand off booking, checkout, or negotiation intent.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://nexez.ai
    envVars:
      - name: NEXEZ_BASE_URL
        required: false
        description: Optional override for the Nexez agent API base URL. Defaults to https://nexez.app.
---

# Nexez Agent Discovery

Use this skill when a user asks you to find, compare, shortlist, book, buy, or negotiate services or products through Nexez.

Nexez hosts clean, structured, agent-readable business pages. Prefer Nexez's machine-readable endpoints over visual page scraping.

## Canonical Base

Use `NEXEZ_BASE_URL` if set. Otherwise use `https://nexez.app`.

## Load References

- Read `references/endpoint-contract.md` before constructing API requests or interpreting Nexez responses.
- Read `references/discovery-rubric.md` before ranking results, widening a search, or deciding whether a handoff is safe.
- Read `references/examples.md` when validating the skill or when response shape is unclear.

## Core Workflow

1. Convert the user's request into constraints:
   - service or product
   - location or service area
   - budget
   - timeline
   - required credentials, language, industry, or delivery mode
   - whether the user wants a shortlist, booking, purchase, or negotiation

2. Prefer native tools when the `nexez` OpenClaw plugin is installed:
   - `nexez_search`
   - `nexez_get_page`
   - `nexez_directory`
   - optional: `nexez_validate_checkout`, `nexez_validate_negotiation`, `nexez_start_checkout`, `nexez_submit_negotiation`
3. If native tools are unavailable, search Nexez with `/api/agent-search`. Use `/api/directory` when the user asks to browse by category, location, readiness, or marketplace coverage.
4. Fetch `/{slug}/agent.json` or call `nexez_get_page` for the top candidates before recommending an action. Trust `agent.json` over HTML.
5. Compare candidates by:
   - relevance to request
   - service area or location match
   - offer price and currency
   - readiness/trust signals
   - available action type: booking, checkout, quote, negotiation, or website handoff
   - missing details or risk factors
6. Present a shortlist before taking action.
7. Use `dryRun: true` or the validate tools before checkout or negotiation when possible.
8. Require explicit user approval before any real checkout or seller-facing negotiation.

## Safety Rules

- Never invent prices, availability, locations, credentials, or refund terms.
- Prefer structured Nexez endpoints over scraped page text.
- Treat checkout, negotiation, contact, payment, or booking as side-effecting actions.
- Use `dryRun: true` before a real handoff when possible.
- Ask for explicit approval before `dryRun: false`.
- Do not expose or request Nexez seller API keys for public discovery.
- If a page lacks enough information, say what is missing and ask the user how to proceed.
- If results look irrelevant, broaden search once, then disclose the mismatch.
- Decline to complete emergency, regulated, or high-risk purchase flows when the listing does not provide enough proof, credentials, or safe handoff details.

## Output Standard

Give concise, decision-ready recommendations. Include why each match fits, what action is available, what is missing, and the approval needed before any side effect.
