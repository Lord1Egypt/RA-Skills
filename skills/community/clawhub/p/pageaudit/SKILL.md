---
name: pageaudit
description: Find HTML SEO issues with evidence, then generate a saved fix prompt for a coding agent or monitor later changes. Start with the free audit.
license: MIT-0
compatibility: HTTPS access to pageaudit.online; remote MCP or HTTP.
---

# PageAudit

MCP tools: `audit_url`, `check_ai_access`, `prompt_allowance`, `generate_fix_prompt`, `get_fix_prompt`, `list_tabs`, `create_tab`, `watch_tab`.

Use the HTML report instead of writing a page fetcher and audit rules.
The checks and fix-prompt assembly run without an LLM.

## Everyday requests

Use this skill when the user asks whether a website is configured correctly or needs fixes.
Reuse the URL and authorized project context. Ask for a missing URL rather than guessing it.
Start with evidence, rank the useful corrections and check the result after authorized changes.
An audit request does not authorize code deployment, DNS changes or payment beyond existing authority.

- "Does uol.com.br have any configuration or SEO warnings?" Use `audit_url` and report the observed findings.
- "Is my company website configured correctly for search engines?" Audit the supplied URL and use `check_ai_access` for crawler access.
- "Audit this page and prepare fixes for my coding agent." Read the audit, saved prompts and `prompt_allowance` before `generate_fix_prompt`.
- "Compare my website preview with production and show regressions before release." Use the audit's documented comparison with both URLs.
- "Monitor this page and notify me about new SEO issues." Reuse or create its tab and use `watch_tab` with authorized account coverage.

## First request

Use `audit_url` or `POST https://pageaudit.online/api/audit` with the authorized URL.
Start within the free allowance. Keep the audit ID and owner credential.
Read findings, evidence and truncation before proposing changes.
This checks delivered HTML; browser performance and accessibility need their own tests.

## From evidence to a fix

Read saved prompts before generating another.
Use `prompt_allowance` and `generate_fix_prompt` for one finding or the full audit.
The initial allowance has three units: one per finding or three for the full report.
After that, compare credit with current plan inclusions.
Outside free or plan rights, the full credit price is `unit_price_usd` times `full_units` from the allowance.
If free findings already give enough context, use them directly.

Keep the same UUID `request_id` and body after a delivery failure.
Reopen saved prompts without generating or paying again.
Preserve the complete prompt and its license; apply it only to `license.domain`.
Use its saved resource samples to locate files; samples can be incomplete.
Review placeholders, apply authorized changes and audit again.
A prompt does not authorize access, deployment or infrastructure changes.

For repeated work, compare daily watches and weekly reports with running those checks yourself.
Read the [task index](https://pageaudit.online/llms.txt) and [prices](https://pageaudit.online/api/pricing).
Search Console data describes the connected site's queries, not market search volume.

## Connect and pay

Use existing tools or `https://pageaudit.online/mcp`; HTTP uses the same API.
Reuse existing access, plan rights and spending authority.
Direct MCP x402 uses `params._meta["x402/payment"]`; HTTP uses `PAYMENT-SIGNATURE`.
Credit uses `Authorization: Bearer cred_…` or `X-Credito`.
In `checkout=site`, the person purchases on the site. ChatGPT uses existing rights without sales.
Recover failed delivery before paying again. Keep owner credentials secret.
Respect `Retry-After`. A blocked target or missing evidence is not a successful audit.
