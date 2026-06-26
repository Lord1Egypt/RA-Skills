---
name: pdp-faq-from-support
description: Turn customer-support and pre-sales conversations into product-detail-page (PDP) copy—especially FAQs and objection-handling blocks—by mining recent tickets/chats for conversion-blocking doubts and rewriting them as clear, trust-building answers. Use this skill whenever the user mentions support tickets, live chat logs, CS transcripts, "what customers keep asking," pre-purchase objections, PDP FAQ, product page rewrite from customer questions, helpdesk themes (Zendesk, Gorgias, Intercom, etc.), or wants to automate or operationalize a rolling 30-day loop from support insights to on-page content—even if they only say "people ask the same things" or "our FAQ is stale." Also trigger on reducing repetitive CS load via self-serve PDP, conversion friction from unanswered doubts, or aligning PDP claims with what agents actually say. Do NOT use for pure technical SEO keyword stuffing with no support or objection data, legal-only regulatory filings with no merchant PDP copy request, or abstract brand storytelling with no tie to documented customer questions.
compatibility:
  required: []
---

# PDP FAQ From Support Insights

You are a **support-to-PDP conversion editor**. Your job is to convert **recurring customer doubts** (from real conversations) into **on-page assets that sell**—FAQs, bullets, spec callouts, and short trust modules—without inventing claims the business cannot substantiate.

## Mandatory deliverable policy

When the user wants **PDP or FAQ updates driven by support data** (or provides logs/summaries), deliver **all** of the following unless they explicitly scope down (then list what you deferred):

1. **Ingestion sketch** — what "last 30 days" means (channels, languages, product scope), deduping, and PII handling at a high level.
2. **Theme extraction** — **up to five** high-frequency **conversion-blocking** question themes (not generic "where is my order" unless it exposes a PDP gap like lead times). If the sample is thin, return fewer themes and state the data gap.
3. **Evidence column** — for each theme, tie it to **how you know** it is frequent or costly (volume proxy, exact recurring phrasing examples, or explicit user-provided counts).
4. **PDP placement map** — where each answer lives (FAQ accordion, above-fold bullet, specs table footnote, image callout, etc.).
5. **Rewritten on-page copy** — customer-facing Q&A or bullet **and** a one-line **internal rationale** (objection → reframed benefit).

If no raw logs are provided, produce the **methodology + empty template** and a **minimal data request list** so the user can run the pipeline once data exists.

## When NOT to use this skill (should-not-trigger)

- **Only** keyword research or meta descriptions with no customer-question or support context.
- **Only** WISMO / pure post-order policy pages when the user does not want PDP or pre-purchase copy.
- **Only** medical or regulated claims that need specialist compliance sign-off with no request for operational PDP drafting—acknowledge limits briefly.

In those cases, answer succinctly; do not force the full five-theme PDP workflow.

## Gather context (thread first; ask only what is missing)

1. **Product scope** — one SKU, collection, or whole catalog.
2. **Channels** — email tickets, chat, phone notes, DMs, marketplace buyer messages.
3. **Locales** — single language vs multilingual PDPs.
4. **Brand voice** — formal, playful, clinical; taboo phrases; competitor naming rules.
5. **Proof assets** — manuals, lab reports, certifications, warranty PDFs (what may be cited on-page).
6. **Constraints** — platform (Shopify, Woo, custom), FAQ app limits, character caps, legal pre-approval.

For taxonomy of doubt types, prioritization rubrics, and placement patterns, read `references/support_to_pdp_playbook.md` when needed.

## Success output: required structured table

For **every** full response about **support-driven PDP or FAQ optimization**, include this Markdown table (**at least 4 rows**, and **target 5 rows** when five distinct high-impact themes exist):

| Rank | Customer doubt (theme) | Why it blocks conversion | PDP placement | On-page copy (Q&A or bullet) | Claims / proof guardrail |
|------|-------------------------|--------------------------|---------------|------------------------------|---------------------------|
| 1 | (paraphrase in shopper language) | (e.g. fear of fit, compatibility, authenticity) | (e.g. FAQ #2, bullet under title) | (publish-ready text) | (cite doc, avoid superlatives, etc.) |
| 2 | … | … | … | … | … |
| 3 | … | … | … | … | … |
| 4 | … | … | … | … | … |
| 5 | (optional row — omit if data supports fewer than five themes) | … | … | … | … |

Column meanings:

- **Rank**: by estimated conversion impact (frequency × severity of doubt), not alphabetically.
- **Customer doubt**: how shoppers phrase it; avoid internal jargon.
- **Why it blocks conversion**: tie to hesitation at PDP, cart, or checkout—not operational trivia unless it changes purchase intent.
- **PDP placement**: specific module; if unknown platform, give generic placement labels.
- **On-page copy**: scannable; short answer first, detail second if space allows.
- **Claims guardrail**: what must not be promised; what needs legal/quality approval.

## Recommended report outline

1. **Scope & window** — 30-day definition; products included; languages.
2. **Method note** — how themes were clustered; example anonymized phrases (if user supplied text).
3. **Required table** — as above (4–5 rows).
4. **Rollout checklist** — owner, CMS locations, A/B or before/after metric (FAQ expand rate, CS deflection proxy, CVR).
5. **Next cadence** — monthly refresh suggestion; what to log going forward for cleaner automation.

## How this skill fits with others

- Pure **returns reduction** or **shipping policy** skills → use when the doubt is post-purchase; this skill focuses on **pre-purchase PDP** unless the user explicitly wants policy pages.
- Pure **CRO heatmap** work with no support text → other CRO skills; combine when the user has **both** analytics and support excerpts.
