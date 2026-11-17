---
name: oo-ploid
description: "Ploid (ploid.com). Use this skill for ANY Ploid request — reading, creating, updating, and deleting data. Whenever a task involves Ploid, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Ploid"
  author: "OOMOL"
  version: "1.0.2"
  services: ["ploid"]
  icon: "https://static.oomol.com/logo/third-party/ploid.svg"
---

# Ploid

Operate **Ploid** through your OOMOL-connected account. This skill calls the `ploid` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Ploid. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ploid" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ploid" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_person_run` — Cancel a deep person run [destructive]
- `cancel_set` — Cancel a running People Set search; keep already admitted people (preview). [destructive]
- `compile_monitor` — Compiles a natural-language query into targets, events and relevance criteria, and derives an output schema when `output.type` is `object` without a schema. Creates nothing. Compile and create cost 1 ACU. Each run costs 1 ACU per target fetched plus 1 ACU per emitted item. Baseline runs emit nothing.
- `create_dataset` — Seed up to 25 rows (sync) or 2000 rows (async) of people, companies, or custom entities, and name up to 30 columns. Every cell is fused from many sources into one answer with a 0..1 confidence and public evidence URLs. Sync requests answer within deadline_ms (default 20000); cells still running at the deadline return status timeout. mode async returns 202 and fills rows in the background; poll GET /v1/datasets/{id} and page rows_url. Pay on hit: 1 ACU per 10 found standard cells (rounded up per request), 1 ACU per found custom cell, 1 ACU per work email, 3 ACU per personal email, 10 ACU per phone. not_found, unverified, and timeout cells are free. The API key reserves the all-found upper bound and releases the rest after the run. Requires people:search. [write]
- `create_harness_chat_completion` — Create a non-streaming chat completion with Ploid model routing and tool definitions. Requires agent:chat. The upstream enforces its current payload and tool limits.
- `create_monitor` — Creates a scheduled monitor over LinkedIn, X, Instagram and TikTok and starts a silent baseline run. `meta.baseline_run_id` identifies that run; `meta.unresolved` lists mentions that could not be turned into a target. Compile and create cost 1 ACU. Each run costs 1 ACU per target fetched plus 1 ACU per emitted item. Baseline runs emit nothing. [write]
- `create_set` — Create a preview People Set and start a durable criteria-verified search. Requires people:search. [write]
- `delete_monitor` — Delete (disable) a monitor [destructive]
- `enrich_person` — Resolve contact fields for one person using a LinkedIn URL, permanent person_id, email (with first and last name at a work domain, or alone for a reverse lookup), or name plus company domain. Request work_email, personal_email, and/or phone; every field reports found, not_found, or unavailable with confidence, source, and last_seen. Responses include explicit usage.billed and usage.not_found. The legacy lightweight LinkedIn profile contract remains supported; use /v1/person for deep public evidence. Requires the people:enrich scope.
- `enrich_social_profile` — Resolve a public profile from a supported platform handle or URL. Requires the people:enrich scope.
- `export_set` — Export admitted People Set items as JSON, preserving raw field values (preview).
- `get_account_profile` — Requires account:read.
- `get_account_usage` — Returns workspace ACU usage plus the calling key's ID, budget, and the number of active keys. Requires account:read.
- `get_credits` — Returns the workspace ACU balance and budget state for the API key used on this request. Requires account:read.
- `get_dataset` — Status, columns, and progress of a dataset owned by the caller's workspace. Requires people:search.
- `get_harness_context` — Returns the calling user's bounded Ploid user, company, and relevant memory context without running a model. Requires agent:chat.
- `get_linkedin_company` — Identity-bound LinkedIn read. Requires the linkedin:read scope.
- `get_linkedin_profile` — Returns a LinkedIn profile by URL, vanity slug, or @handle. Requires the linkedin:read scope.
- `get_monitor` — Get a monitor
- `get_monitor_run` — Get a run
- `get_open_api_document` — Returns this OpenAPI 3.1 contract. No authentication is required.
- `get_person` — Resolve one reviewed deep person profile. An eligible cached profile returns 200, including stale data with a queued refresh. Unseen people and snapshots requiring new review return a durable 202 run. Fresh research can take minutes; poll the returned run ID. A completed uncertain identity returns data:null with meta.resolution=unsure and reason ambiguous_identity or insufficient_evidence. The first successful profile costs exactly 25 ACU on every plan; organization-wide rereads are free for 90 days. Failed, uncertain, and not-found runs are free. Current role fields, age, and social audience/activity metrics are not populated by the current reviewed projection. [write]
- `get_person_run` — Poll a deep person run
- `get_set` — Read a People Set and its searches, newest first. Inspect searches for progress and stop_reason (preview).
- `list_company_recruiters` — Merges live LinkedIn search, web search results, and the Ploid people index to return recruiters, role counts, and whether each count is complete. Placeholder company names are skipped. Up to 10 companies per request; each unique non-placeholder company is billed for returned matches. Requires people:search.
- `list_dataset_rows` — Rows in seed order with their cells. Usable while an async dataset runs; pending rows report timeout cells until filled. Requires people:search.
- `list_linkedin_company_posts` — Identity-bound LinkedIn read. Requires the linkedin:read scope.
- `list_linkedin_posts` — Returns recent posts for a LinkedIn profile. Requires the linkedin:read scope.
- `list_linkedin_profile_comments` — Identity-bound LinkedIn read. Requires the linkedin:read scope.
- `list_monitor_items` — List emitted items
- `list_monitor_runs` — List runs
- `list_monitors` — List monitors
- `list_set_items` — Page admitted people from a People Set, including partial results while a search runs (preview).
- `list_sets` — List the most recent workspace People Sets (preview). Requires people:search.
- `resolve_person` — Identify one person from a full name plus at least one clue (company name or domain, role, location, address, work or personal email, or phone) by fusing the people index with live web results. Returns the permanent person_id accepted by /v1/person and /v1/enrich, so a deep profile is only bought for the right person. Costs 2 ACU when a person is found; no match is free. A match is model-assessed, not identity-verified. Requires people:search.
- `revoke_current_api_key` — Immediately revokes the calling API key. A successful response is the final response that key can authorize. Requires account:read. [destructive]
- `run_monitor` — Trigger a run now [write]
- `search_github_accounts` — Filter Ploid's GitHub accounts index. Every criterion is AND; give at least one. Results come back by relevance when query or company is set, otherwise by merged pull requests and then commits; sort picks an activity ranking instead. Page with offset up to 1000 results deep; the last page before that shrinks to fit, so next_offset can always be followed with the same limit. With include_profiles, each account also carries its live public GitHub profile (limit defaults to and may not exceed 10). Costs 1 ACU per completed search plus 1 ACU per live profile found, charged together; failed searches are not charged. Emails and phone numbers are never returned. Requires people:search.
- `search_github_people` — Run a GitHub accounts search, read each account's live public profile, and tie it to a LinkedIn profile: one the user lists on GitHub, or the one indexed person whose name matches and whose employer or location agrees. Ambiguous matches are left unlinked. linkedin filters are hard: a person is returned only when their linked, indexed LinkedIn profile satisfies every one. Pages advance over GitHub accounts (scanned), so a page can return fewer people than it scanned; follow next_offset. At most 10 accounts per page. Costs 1 ACU per completed search plus 1 ACU per returned person, charged together; failed searches are not charged. Emails and phone numbers are never returned. Requires people:search.
- `search_linkedin_people` — Structured LinkedIn people search by keywords, location, title, company, and school. Requires the linkedin:read scope.
- `search_people_candidates` — Return up to 10 basic indexed profiles matching all name terms plus optional company, location, and title filters. Requires people:search; legacy full-access keys with both people:enrich and agent:chat are accepted. Costs 1 ACU per completed search, including zero matches; failed searches are not charged. Never starts research or enrichment. Normal account billing, auto-recharge settings, and API-key spending caps apply. Send an Idempotency-Key to replay a request without another charge. Indexed identities and employment are unverified. Ask the user to choose before POST /v1/person, which costs 25 ACU unless the workspace already has active access. One bounded index request; no exhaustive count or pagination. Workspace limits: 30 requests/minute and 300/hour across keys. Active account eligibility still applies.
- `start_dataset` — Start an asynchronous dataset to fill up to 2000 rows with sourced column values. Requires people:search. [write]
- `sync_people_search` — Retrieve up to 150 people inline per request; async:true or a larger num_results starts a background People Set instead and returns 202 with set_id, items_url and events_url. instant returns indexed candidates as ranked by the index. fast compiles the query, reads a pool of at least 200 indexed candidates (three times num_results when that is larger) and ranks them by the stated role, place, employer, keywords, industry and seniority before returning the first num_results, without web verification. auto and deep research the complete query and explicit filters before returning matches with verification references; uncertain and rejected candidates are excluded from results, grounding and billing. Auto/deep compile the query, verify candidates, and run one bounded web recovery pass when too few match. Each verification pass permits up to 30 seconds for auto or 45 seconds for deep; recovery discovery permits 45 or 60 seconds respectively; the whole verification stage answers within 60 seconds for auto and 120 seconds for deep. A partial status means the requested count was not filled or verification hit its deadline; coverage.has_more says more candidates remained. Use Sets for durable research of large result sets. Verification is evidence-based model assessment, separate from identity verification. Requires people:search. [write]
- `test_monitor` — Dry run. Fetches the monitor's targets now, judges recent activity against the query, and returns up to max_items_per_run relevant items, newest first. Nothing is saved: no run, no items, no seen-ledger or snapshot change, no webhooks, and the schedule is untouched. `already_seen` marks items an earlier run already recorded, which a real run would not send again. Works before and after the baseline. Costs 1 ACU per target fetched; no item or output-extraction charge (items carry `source`, not `output`).
- `test_monitor_webhook` — Posts a `monitor.webhook.test` event to webhook_url right away, signed with webhook_secret when set, and returns the HTTP outcome. One attempt, no retries, no ACU. [write]
- `update_account_profile` — Requires account:write. [write]
- `update_monitor` — Changing `query` recompiles the plan; passing `plan` replaces the targets. Either starts a new baseline run. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Ploid state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Ploid is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/ploid
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Ploid homepage: https://ploid.com
- API documentation: https://ploid.com/documentation/getting-started/authentication
