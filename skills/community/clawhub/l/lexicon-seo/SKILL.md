---
name: lexicon-seo
description: Run technical SEO and AI-visibility audits through Lexicon SEO's hosted MCP server (start audits, read reports, list issues, verify page fixes, citations, content refresh drafts). Use when the user asks to audit a site, check indexing or on-page SEO issues, pull Lexicon fix steps, recheck a page, review AI citation readiness, or draft title/meta/H1 refreshes via Lexicon.
metadata:
  author: Lexicon SEO
  version: "1.0.0"
  homepage: https://lexiconseo.com
  openclaw:
    homepage: https://lexiconseo.com/docs/mcp/
    emoji: "📗"
    requires:
      env:
        - LEXICON_API_KEY
    primaryEnv: LEXICON_API_KEY
    envVars:
      - name: LEXICON_API_KEY
        required: true
        description: Bearer API key from the Lexicon dashboard (Starter, Professional, or Business). Create at https://lexiconseo.com/app/settings/
compatibility: Requires a paid Lexicon SEO account, network access to https://lexiconseo.com/mcp, and an MCP client configured with Authorization Bearer (Claude Code, Cursor, Claude Desktop, or equivalent).
---

# Lexicon SEO

**Words matter.** Lexicon SEO audits public sites for technical SEO and AI visibility. This skill teaches an agent how to use Lexicon’s **hosted** MCP tools. It does not run a local crawler.

Canonical docs: https://lexiconseo.com/docs/mcp/

## When to use

- User wants a Lexicon audit of a public website
- User asks what SEO issues a Lexicon report found, or how to fix a Lexicon issue code
- User wants to recheck one page after a fix (`verify_fix`)
- User asks about AI citation / answer-readiness results already stored on a report
- User wants a draft title, meta description, or H1 refresh from a finished audit

## When not to use

- No Lexicon API key / Free plan only (MCP returns an upgrade error)
- User wants Google Search Console or Bing Webmaster Tools changes Lexicon cannot perform from MCP alone
- User asks to **publish** content — `refresh_page` drafts only; it does not publish
- Site-wide checks (for example robots.txt policy) via `verify_fix` — use `start_audit` instead

## Prerequisites

1. Paid Lexicon plan: Starter, Professional, or Business — https://lexiconseo.com/pricing/
2. API key from Settings — https://lexiconseo.com/login/?next=/app/settings/ (shown once; Lexicon stores a hash)
3. MCP client pointed at `https://lexiconseo.com/mcp` with `Authorization: Bearer <key>`
4. Never print, log, or commit the API key

Rate limits (per key): Starter 30/min, Professional 60/min, Business 120/min.

## Typical workflow

1. **`list_sites`** — see monitored and previously audited hosts for this account.
2. **`start_audit`** with `{ "url": "https://example.com" }`.
   - Uses one audit from the monthly allowance.
   - If the tool quotes credits, show the quote and only call again with `"confirm": true` after the user agrees.
3. Poll **`get_audit_status`** with `{ "id": "<audit-id>" }` until status is no longer running.
4. **`get_report`** with `{ "id": "<audit-id>", "format": "markdown" }` (or `"json"`).
5. **`list_issues`** with `{ "report_id": "<audit-id>" }` — optional `severity`: `critical` / `warning` / `info` (or `P0` / `P1` / `P2`).
6. **`get_fix`** with `{ "issue": "<code>", "report_id": "<audit-id>" }` for steps.
7. After the user ships a fix on one URL, **`verify_fix`** with `{ "url": "...", "issue_code": "..." }` (no audit consumed). Refuse site-wide codes; tell the user to run `start_audit`.
8. Optional: **`get_citations`** / **`extra_citation`** (extra cites quote price first; confirm to spend).
9. Optional: **`refresh_page`** then **`get_refresh`** for drafts (allowance / confirm; 30-day reuse per page; Business may include one section draft).

## Spending rules

- Never set `confirm: true` unless the user explicitly approved the quoted spend.
- `start_audit`, `extra_citation`, and `refresh_page` can quote credits after plan allowances.
- Say clearly when a call would use an audit slot or credits.

## Reporting rules

- The report **score is a Lexicon heuristic**, not a Google ranking score.
- Do not invent metrics, customer counts, rankings, or citation guarantees.
- Prefer Lexicon’s own wording from `get_report` / `get_fix` over paraphrasing that changes meaning.
- If a tool returns an error JSON, surface that error; do not invent a successful result.

## Support

- Docs: https://lexiconseo.com/docs/mcp/
- Product: https://lexiconseo.com
- Email: support@lexiconseo.com
