# Paid Actions

Read this for `PAID_ACTION`: unlock, cross-company contact search, or sending email.

## Contents

1. Non-Bypassable Rules
2. Company Unlock
3. Contact Search
4. Email Send
5. Balance and Local State
6. Missing Batch Recovery

## 1. Non-Bypassable Rules

- Free company search is allowed without paid confirmation.
- Unlock selected companies requires explicit credit confirmation before the selected unlock batch runs.
- Cross-company `POST /contacts/search` requires first-session confirmation that it costs 1 credit per query.
- Email send requires explicit recipient and content confirmation.
- Profile, Web Research, Expansion, result review, and search strategy cannot authorize paid actions.

## 2. Company Unlock

When the user chooses displayed rows or when you recommend a concrete unlock set, first prepare an internal unlock plan. This is a background mechanism, not an extra user-visible confirmation step:

```bash
node scripts/prepare-unlock-plan.js --selection-handle '<selection_handle>' --rows 1,3,5 --compact --locale '<user-locale>' --debug-metadata
```

For a processed final unlock target set, such as model recommendations, filtered priority groups, sorted candidates, observe-to-unlock changes, multi-page consolidation, or user edits before confirmation, write a small JSON file containing only script-owned source references:

```json
{
  "selections": [
    { "selection_handle": "sel_...", "rows": "1,3,5", "reason": "priority fit" },
    { "selection_handle": "sel_...", "rows": "2", "reason": "user added" }
  ]
}
```

Then freeze it with:

```bash
node scripts/prepare-unlock-plan.js --selection-set-file /private/tmp/okki-go-batches/<target-set>.json --compact --locale '<user-locale>' --debug-metadata
```

Use the script-provided `selected_companies` to phrase the normal confirmation. Do not show `unlock_plan_id` to the user.

Ask once for the prepared unlock batch. The batch may contain one row or multiple displayed rows:

```text
Unlocking the selected N companies costs up to N credits, 1 credit per company unless it was unlocked in the last 30 days. Proceed?
```

A row selection is not confirmation. Preparing an unlock plan is not confirmation. After the user accepts the batch credit cost, run one wrapper command for the confirmed plan; do not ask again for each internal `/companies/unlock` request made by the wrapper.

If the user changes the final target set before confirmation, prepare a new unlock plan and discard the previous confirmation boundary. Old plans are invalidated by active-plan state and must not be executed.

After confirmation:

```bash
node scripts/unlock-companies.js --plan '<unlock_plan_id>' --mark-unlocked --compact --locale '<user-locale>' --artifact-dir '<agent-visible-output-dir>'
```

Pass `--artifact-dir` when the Agent has a writable workspace/artifacts/outputs directory. The wrapper does not request filesystem permission during paid unlock. It preflights the details Markdown path before paid API calls, falls back to internal temporary storage with a warning when the artifact path is not writable, and fails before paid API calls only when no details Markdown path is writable.

If the wrapper returns `error_code: "DETAILS_MARKDOWN_PRECHECK_FAILED"` with `next_action: "authorize_artifact_dir"`, tell the user the unlock did not run and no credit was charged because no details-document path was writable. Ask whether the Agent should help authorize a writable folder or retry with another already-writable directory.

Report:

- script-provided plan/success/failure counts
- charged count or whether no credit was charged
- remaining balance when available
- script-rendered `unlock_details_markdown` exactly as the chat display
- Markdown detail document path containing all unlocked company details when it is not already visible in `unlock_details_markdown`
- artifact access note and fallback warnings
- warnings

After selected-company unlock, the normal next step is drafting outreach from the unlocked company/profileEmails data when useful. Do not present paid `contacts/search` as the normal next step; use it only when the user explicitly asks for cross-company contact search.

Field ownership, raw/debug behavior, and private metadata handling are governed by `output-contracts.md`. Free-search domains stay hidden, but unlocked company details may show `display_website` derived from profile website/domain or saved search domain.

## 3. Contact Search

Before the first contact search in a session:

```text
Contact search costs 1 credit per query. Do you want to continue?
```

After confirmation:

```bash
node scripts/search-contacts.js --json '<contacts/search payload>' --save-batch /private/tmp/okki-go-batches/<contacts>.json --compact
```

Default visible size is 20 unless the user asked for more; wrapper requests may use `size` up to 100. Report script-provided contact rows, counts, and charge summary without filtering or renumbering them. Save raw contact results when many contacts are requested; field ownership follows `output-contracts.md`.

## 4. Email Send

Drafting is free. Sending consumes EDM quota.

Before sending:

1. Show recipient summary.
2. Show or reference the content to be sent.
3. Ask for explicit confirmation of both recipients and content.

After confirmation:

```bash
node scripts/send-email.js batch --json '<payload>' --mapping-file /private/tmp/okki-go-batches/email-send.json --compact
node scripts/send-email.js personalized --file /private/tmp/personalized-send.json --compact
```

Post-send output should use the script-provided task IDs, counts, status, and next status-check command. Do not echo full bodies unless requested.

## 5. Balance and Local State

Balance is free:

```bash
OKKIGO_API_KEY="$(bash scripts/resolve-api-key.sh --print)"
curl -s -X GET "${OKKIGO_BASE_URL:-https://go.okki.ai}/api/v1/credit/balance" \
  -H "Authorization: ApiKey ${OKKIGO_API_KEY}" \
  -H "X-Okki-Skill-Version: ${OKKIGO_SKILL_VERSION:-1.3.2}"
```

`--mark-unlocked` only updates local viewed state. If local state write fails after unlock succeeds, tell the user the company was unlocked but local viewed records were not updated. Do not repeat the paid unlock.

## 6. Missing Batch Recovery

Selection handle or unlock plan reuse does not bypass confirmation.

If selection or plan mapping is missing, unreadable, or stale:

1. Explain that the private row mapping is unavailable.
2. Re-run a free lookup or ask the user to choose from a new displayed list.
3. Ask explicit paid confirmation before unlocking.
