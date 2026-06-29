# Output Contracts

This reference owns compact stdout, detail, debug metadata, raw/export behavior, and field ownership across OKKI Go wrappers.

## Contents

1. Output Classes
2. Field Ownership
3. Wrapper Contracts
4. Routing Hints
5. Migration Rule

## 1. Output Classes

| Class | Use when | Model-visible behavior |
|---|---|---|
| Normal compact | Default for user workflows. | Answer-ready rows, short summaries, routing hints, and actionable warnings only. |
| Detail | User asks for fuller user-facing detail. | More profile/contact/status fields, still sanitized. |
| Debug metadata | User asks for debug, paths, IDs, budget details, or implementation details. | Use `--debug-metadata`; output appears under `debug_metadata`. |
| Raw/export | User explicitly asks for raw/export or tests require it. | Save raw data to files; print paths and concise summaries rather than large payloads when possible. |

## 2. Field Ownership

| Field or concept | Owner | Normal compact rule |
|---|---|---|
| `domain` | Scripts and saved batch/raw files. | Do not print; model does not copy or preserve it. |
| raw IDs / `companyHashId` / contact IDs | Scripts and raw/debug output. | Do not print. |
| free-search ID vs `companyHashId` | Scripts. | Free-search ID/raw `id` is never a `companyHashId`; the only valid source for `companyHashId` is the `/companies/unlock` response. |
| `batch_id` | Scripts derive from saved path/latest pointer. | Under `debug_metadata` only. |
| `raw_path` | Scripts. | Under `debug_metadata` only; raw is still saved. |
| `private_mapping_saved` | Scripts. | Under `debug_metadata` only. |
| `output_budget` | Scripts. | Under `debug_metadata` only; keep `returned`, `available`, `truncated`, and `next_offset` in normal output. |
| `selection_handle` | Scripts. | Opaque normal compact handle for preparing paid unlock plans; it must not encode domain, raw path, or IDs. |
| `unlock_plan_id` | Scripts. | Under `debug_metadata` only; use it internally after explicit paid confirmation. |
| final unlock target set | `prepare-unlock-plan.js` and `batch-state.js`. | Prepared from script-owned `selection_handle + rows` references; not from model memory, `latest`, domains, or IDs. |
| `target_set_fingerprint` | Scripts. | Under `debug_metadata` only; active-plan state invalidates old plans when the final target set changes. |
| `available` / `next_offset` / `truncated` | Scripts. | May appear when needed for pagination. |
| `discovery_health` / `health_action` | Scripts. | May appear when needed for pagination, recovery, diagnosis, or Expansion routing. |
| structured presentation | Scripts for tables/details; model for prose around them. | Preserve script-owned fields, order, row set, cardinality, and counts unless the user explicitly asks for a custom summary or comparison. |
| latest batch pointer | `batch-state.js`. | Free follow-up compatibility only; do not use it as the normal paid unlock execution target. |
| unlock plan | `batch-state.js` and `prepare-unlock-plan.js`. | Prepared after row selection; normal confirmation prose may use `selected_companies`, but execution uses hidden `unlock_plan_id`. |
| user-facing artifact | Scripts. | `details_markdown_path` is the selected-company unlock Markdown artifact. Prefer Agent-provided writable artifact directories; raw/audit/private mappings remain internal. |
| local viewed state | `okki-state.js` and unlock helper. | Warnings only; write failure does not invalidate successful unlock. |
| user-facing explanation | Model. | Same language as user; no raw/private fields. |

## 3. Wrapper Contracts

When Context Firewall is active, the Output Renderer Lock allows only the wrapper compact output, the current Action Envelope, the user's latest request, and minimal digest facts needed for one-sentence explanation. Full PDFs, web notes, spreadsheets, raw API JSON, and old unreferenced batches must not shape the primary display.

Company discovery:

- normal compact: `display_table_markdown` plus `rows`, localized country names, `has_email`, `has_whatsapp`, `available`, `next_offset`, `truncated`, `discovery_health`, `health_action`, `next_action`, and opaque `selection_handle`
- free-search result table: scripts render `display_table_markdown` with localized fixed columns `row`, `company_name`, `country_name`, `company_type`, `fit`, `has_email`, `more_info`; `more_info` displays WhatsApp availability, employee count, and founding time with labels; the model does not rebuild, filter, reorder, renumber, or recount it
- this display rule applies to every mode that runs a new free company search, including L0, L2 recovery/strategy, and Expansion
- recommendation groups and coaching are analysis overlays after the table; they do not replace the table
- debug metadata: raw path, batch ID, private mapping flag, output budget
- raw file only: domains, IDs, raw API rows, exact email counts, exact WhatsApp counts
- next user action: model writes natural-language guidance after the table based on `next_action` and `discovery_health`

Unlock plan preparation:

- normal compact: `selected_companies`, `max_credit_cost`, `paid_confirmation_required`, and concise confirmation boundary
- processed target set compact input: `--selection-set-file` accepts multiple `selection_handle + rows` entries for recommendations, filtering, ranking, multi-page consolidation, and user edits
- debug metadata: `unlock_plan_id`, source batch ID or target-set fingerprint, output budget
- raw/private plan file only: domains, batch path, and private row mapping
- user-facing behavior: no extra confirmation step; use `selected_companies` to phrase the existing paid confirmation

Selected-company unlock:

- normal compact: script-rendered `unlock_details_markdown` for chat display, `run_status`, `planned_count`, `success_count`, `failed_count`, `stopped_count` only when positive, charged count, balance when available, `company_details` compatibility data for at most 5 successful companies, `details_markdown_path` for all unlocked company details, `details_markdown_artifact`, `artifact_dir`, `artifact_access_note`, warnings, and `next_action`: `draft_outreach` when at least one company unlock succeeds
- debug metadata: raw path, batch ID, output budget
- raw file only: domains, company hash IDs, raw profile/email payloads
- companyHashId provenance: do not use free-search ID, raw `id`, row number, domain, or model memory as `companyHashId`; profile/profileEmails lookups use only the hash returned by `/companies/unlock`
- chat display: `unlock_details_markdown` uses vertical tables for at most 5 successful companies and includes the full `details_markdown_path`; the top summary shows planned, success, failure, charge, and balance only; it does not expose attempted/not-attempted counters; the model does not rebuild it from `company_details`
- failure or not-executed rows appear only when they exist, as script-rendered concise rows; the model does not invent fixed failure sections
- user-facing detail artifact: `details_markdown_path` uses the full detail-block Markdown template for all successful companies and concise failure rows when present; no normal JSON export recommendation. `--markdown-file` wins, then `--artifact-dir`, then `OKKIGO_ARTIFACT_DIR`, then current working directory `okki-go-artifacts/`, then internal temporary storage.
- artifact preflight: before paid unlock calls, the wrapper verifies a writable details Markdown path. If an explicit or default artifact path is not writable, it falls back to the internal temporary path and emits a warning without asking for permission. If no details Markdown path is writable, it exits before paid API calls with `error_code: "DETAILS_MARKDOWN_PRECHECK_FAILED"`, `paid_api_called: false`, `unlock_executed: false`, `next_action: "authorize_artifact_dir"`, and `recovery_suggestion`.
- Do not present paid `contacts/search` as the normal next step after selected-company unlock; unlocked company `profileEmails` data is already fetched without a separate contact-search confirmation
- local state failure: warning only

Contact search:

- normal compact: script-provided contact rows, role/company/country/email availability, and charge type summary; balance is not included
- debug metadata: raw path, batch ID, output budget
- raw file only: raw contact IDs and payloads

Email send:

- normal compact: script-provided submitted status, task IDs, total, accepted/rejected counts when derivable, and next status-check command
- hidden/detail: full email body unless explicitly requested

Email status:

- normal compact: script-provided summary counts, failed rows and reasons, task/mail statuses
- detail: single mail body only when explicitly requested

Local state:

- normal compact: updated/skipped counts and warnings
- raw/debug: full state only on explicit request

## 4. Routing Hints

Allowed `health_action` values:

- `show_results`
- `fetch_next_page`
- `run_light_recovery`
- `ask_refinement`
- `offer_guided_strategy`
- `offer_expansion`

Allowed `next_action` values should be small and imperative, for example:

- `ask_unlock_selection`
- `ask_paid_confirmation`
- `paginate_next`
- `offer_refinement`
- `check_email_status`
- `draft_outreach`
- `authorize_artifact_dir`

Add hints only when they remove real model guesswork.

## 5. Migration Rule

For script-owned metadata currently emitted in compact stdout:

1. Keep it in normal compact only if it is answer-critical or routing-critical.
2. Move it to debug metadata if it only helps debugging or tests.
3. Suppress it if latest batch state or another script-owned mechanism makes it redundant.

Do not replace deterministic script ownership with prompt instructions telling the model to copy, cache, hide, or transform private fields.
