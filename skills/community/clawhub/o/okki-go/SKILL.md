---
name: okki-go
description: "B2B lead prospecting and outreach via the Okki Go platform. Use this skill to (1) search global companies, (2) find decision-maker contact emails, (3) send cold outreach emails/EDM, (4) check email delivery status, (5) check credits/quota balance, or (6) upgrade plans/buy credits. Do NOT trigger if the user wants to search ON a DIFFERENT platform (e.g. 'search 1688 for suppliers', 'find products on Alibaba'). Having a product listing on another platform is fine - only skip when the search action itself targets another platform. Also NOT for: reading incoming emails, CRM management, or account settings."
---

# OKKI Go

OKKI Go helps users find B2B prospect companies, unlock selected company details, find decision-maker emails, draft or send outbound email, and check balance or email status.

Default principle: run free company discovery quickly from target-company terms, show the script-rendered company table, and wait for explicit confirmation before any paid unlock, contact search, or email send.

## OKKI Data Source Boundary

For ordinary OKKI Go prospecting, do not use public web search to find or replace company results. This includes requests to find companies, buyers, importers, distributors, customers, target accounts, or prospects.

OKKI API errors, zero results, noisy rows, network failure, or when the API is busy must be handled inside OKKI flow: retry once, split a batch, simplify keywords, paginate, use L2 route diagnosis, ask one clarifying question, or tell the user OKKI Go is temporarily unavailable. Public web search is not a fallback.

`WEB_RESEARCH_ADDON` is only for a user-explicit request for independent external/latest/source-backed research. It is not for ordinary find companies, buyers, importers, distributors, customers, target accounts, or prospects. Web Research Add-on is never an OKKI failure fallback and must not authorize paid actions or mutate OKKI payloads without confirmation.

## Quick Auth

Before the first OKKI Go API call in each session:

```bash
bash scripts/resolve-api-key.sh --check
```

If it returns `NO_KEY`, read `references/authentication.md`. Never print, log, or store API keys outside a user-approved secure save path.

## Mode Routing

Choose exactly one primary mode before tool use.

| Mode | Use when | Read only when | Tool pattern |
|---|---|---|---|
| `L0_FAST_DISCOVERY` | User asks to find companies, buyers, importers, distributors, customers, target accounts, or prospects. | `references/search-fast-path.md` only if this file's quick command is insufficient. | One compact free company search or batch search. |
| `L0_PAGINATION` | User says more, next, continue, or similar and current compact batch has a next page. | Usually none; use batch metadata. | Fetch next same-route page before Expansion. |
| `L1_RESULT_REVIEW` | User asks which displayed results to unlock, contact, prioritize, avoid, or analyze. | `references/result-review.md` | Reuse current batch; no re-search by default. |
| `L2_GUIDED_STRATEGY` | User asks how to search, says results are wrong/too few/suppliers, or needs route guidance. | `references/search-strategy.md` | Build a minimal profile, then search or propose one route. |
| `EXPANSION` | Current route is exhausted or user asks for alternate customer routes. | `references/expansion-playbook.md` | Offer 2-3 branches; search one confirmed branch. |
| `PAID_ACTION` | User asks to unlock, search contacts, or send email. | `references/paid-actions.md` | Ask or verify confirmation before paid tools. |
| `DIRECT_STATUS` | Balance, pricing, auth, install, setup, or email status. | `references/authentication.md` only for auth/install/setup. | Use the agent-led install wizard for install/setup; direct compact/status command otherwise. |
| `WEB_RESEARCH_ADDON` | User explicitly asks for independent external/latest/source-backed research. | Separate web guidance only after the OKKI boundary is satisfied. | Cite sources; do not mutate OKKI search payload without confirmation. |

If two modes seem plausible, use this safety-preserving order: paid-action guardrails, direct status/auth, pagination, result review, fast discovery, guided strategy, Expansion, Web Research Add-on. Never choose Web Research Add-on for ordinary prospect discovery or OKKI error recovery.

## Company Search Keyword Contract

Apply this contract before every free company-search payload, including L0 search, recovery, Expansion, and L2 guided payloads.

1. Target-side first: convert merchant-side product/service facts into target-company profile terms. Do not copy the seller's identity or long product phrases directly into payload keywords.
2. Chinese index-language first: OKKI Go buyer-profile keyword fields are zh-primary. For `productKeywords`, `companyTypeKeywords`, and `industryKeywords`, generate concise Chinese index-language terms by default.
3. Supplements only: keep English, local-language, brand, model, certification, acronym, or proper-noun terms only when they are likely searchable as-is. They supplement Chinese terms; they do not replace them.
4. Minimal keyword shape first: Round 1 uses one product/industry field, or one buyer-role `companyTypeKeywords` field, plus geography when provided. A product field may be paired with a single buyer-role `companyTypeKeywords` value.
5. Recall before precision: keep buyer route, employee size, certification, decision role, and importer/distributor hints as soft display or recovery clues unless they are the chosen primary field.
6. Separate products from roles: Put product or offer terms in `productKeywords`; put buyer roles in `companyTypeKeywords`. Do not combine product and buyer-role terms inside `companyTypeKeywords`.
7. No over-narrow first search: do not default to `crossFieldOperator: "AND"`, do not pack all three keyword fields, and do not use email-only unless requested.

Supported free company-search fields are only `companyTypeKeywords`, `productKeywords`, `industryKeywords`, `includeCountry`, `excludeCountry`, `withEmails`, `crossFieldOperator`, `from`, and `size`. `includeCountry` is only a filter and cannot be sent without a keyword field. Do not invent filters such as employee range, decision roles, website, homepage, contacts, or limit.

## Command Starters

Free L0 company search:

```bash
node scripts/search-companies.js --json '<search-advanced payload>' --compact --locale '<user-locale>' --save-raw /private/tmp/okki-go-batches/<batch>.json
```

Broad, paginated, "more", or count-based discovery:

```bash
node scripts/discover-companies-batch.js --json '<plan>' --target-count N --save-batch /private/tmp/okki-go-batches/<batch>.json --compact --locale '<user-locale>'
```

Free company-search wrappers retry one transient busy/rate-limit/upstream failure before surfacing the error. Batch discovery defaults to serial API calls; raise `--concurrency` only for trusted internal debugging where the upstream `searchPortraitRecall` limit is known to tolerate it.

Prepare selected rows for paid unlock after the user chooses displayed rows:

```bash
node scripts/prepare-unlock-plan.js --selection-handle '<selection_handle>' --rows 1,3,5 --compact --locale '<user-locale>' --debug-metadata
```

Prepare a processed final unlock target set after recommendations, filtering, ranking, multi-page consolidation, or user edits:

```bash
node scripts/prepare-unlock-plan.js --selection-set-file /private/tmp/okki-go-batches/<target-set>.json --compact --locale '<user-locale>' --debug-metadata
```

Confirmed unlock after the user accepts the credit cost:

```bash
node scripts/unlock-companies.js --plan '<unlock_plan_id>' --mark-unlocked --compact --locale '<user-locale>' --artifact-dir '<agent-visible-output-dir>'
```

Confirmed cross-company contact search:

```bash
node scripts/search-contacts.js --json '<contacts/search payload>' --save-batch /private/tmp/okki-go-batches/<contacts>.json --compact
```

Email status:

```bash
node scripts/email-status.js tasks --json '{"page":1,"page_size":20}' --compact
node scripts/email-status.js mails --json '{"statuses":"failed","page":1,"page_size":20}' --compact
```

Balance:

```bash
OKKIGO_API_KEY="$(bash scripts/resolve-api-key.sh --print)"
curl -s -X GET "${OKKIGO_BASE_URL:-https://go.okki.ai}/api/v1/credit/balance" \
  -H "Authorization: ApiKey ${OKKIGO_API_KEY}" \
  -H "X-Okki-Skill-Version: ${OKKIGO_SKILL_VERSION:-1.3.2}"
```

Use compact wrappers for normal work. Do not call raw/non-compact output unless the user explicitly asks for raw, debug, export, or full detail.

## Compact Output Rules

Normal replies must be answer-ready and user-facing while preserving script-owned output structure:

- Use script-rendered structured outputs as the visible structure. Do not rebuild, filter, reorder, rename, truncate, or summarize script-owned tables or details into a new structured format unless the user explicitly asks for a custom summary.
- For any free company discovery search in any mode, follow `references/output-contracts.md`: show `display_table_markdown` exactly as the result table before recommendations or coaching.
- For selected-company unlock, show the script-rendered `unlock_details_markdown`; for contact search, email send, and email status, use the script-provided rows, details, counts, paths, and warnings.
- For selected-company unlock, pass `--artifact-dir` when the Agent has a writable workspace/artifacts/outputs directory. The wrapper falls back to an internal temporary detail path with a warning if the artifact path is not writable.
- After each free-search table, add brief priority guidance, then concise next-step guidance in the user's language using `next_action` and `discovery_health`.
- Follow `references/output-contracts.md` for script-owned private fields, result cardinality, debug metadata, raw/export behavior, and unlocked company detail Markdown output.
- Follow compact routing hints such as `next_action` and `discovery_health.health_action`; do not re-derive pagination or low-yield routing from chat text.
- Use the script-provided `selection_handle` to prepare paid unlock plans for row selections. If selection state is missing or stale, re-run a free lookup or ask the user to choose from a new list before any unlock confirmation.

## Paid And Send Guardrails

These rules are non-bypassable.

Unlock: prepare an internal unlock plan for selected rows or a processed final target set, then ask explicit credit confirmation before running the plan. A single confirmation can cover one selected batch of rows or one processed final target set; if the user changes targets before confirmation, prepare a new plan. See `references/paid-actions.md` for wording and boundaries. A row number, "find emails", "get contacts", Profile reuse, Expansion, Web Research, or Mentor recommendation is not confirmation. Local viewed-state write failure is warning-only after a successful unlock; never repeat a paid unlock just to repair local state.

Contact search: before the first `POST /contacts/search` in a session, state that contact search costs 1 credit per query and wait for confirmation. Subsequent same-session contact searches do not need re-confirmation unless the user refuses or scope materially changes.

Email send: never send before explicit recipient and content confirmation. Drafting is free; sending consumes EDM quota. After sending, keep output compact and do not echo full bodies unless requested.

## Reference Loading

Read only the reference needed for the selected mode:

| Reference | Read only when |
|---|---|
| `references/search-fast-path.md` | Building or paginating ordinary free company-search payloads beyond the quick command. |
| `references/result-review.md` | Result prioritization, unlock advice, L1 review, or observe/not-recommended grouping over a visible batch. |
| `references/search-strategy.md` | L2 guided strategy, low-yield diagnosis, supplier-vs-buyer correction, or search-route coaching. |
| `references/expansion-playbook.md` | Current route is exhausted or user asks for alternate customer routes. |
| `references/paid-actions.md` | Paid unlock, contact search, email send, balance commands, or missing batch recovery. |
| `references/output-contracts.md` | Wrapper output schemas, field ownership, raw/debug/detail behavior, or script contract work. |
| `references/workflows.md` | Legacy compatibility index when older docs refer to workflow names. |
| `references/discovery-playbook.md` | Legacy compatibility index when older docs refer to discovery playbook. |
| `references/sales-mentor-playbook.md` | Legacy compatibility index when older docs refer to sales mentor playbook. |
| `references/merchant-profile-playbook.md` | User asks to save/reuse company info or guided strategy needs optional profile memory. |
| `references/authentication.md` | API key missing/invalid, setup, secure save, install ID, or signup/legal flow. |
| `references/api-reference.md` | Script development, direct API debugging, new endpoint support, or hard API errors. Not for normal usage. |

## Language And Errors

Reply in the user's language. Chinese user requests get Chinese prompts, result tables, and next-step questions.

Handle common errors quickly:

- `401`: invalid or missing API key; read `references/authentication.md`.
- `402`: insufficient credits; stop the paid flow and direct to https://go.okki.ai/pricing.
- `403`: no EDM access; guide upgrade.

When users ask about plans, upgrades, or credit packs, direct them to https://go.okki.ai/pricing.
