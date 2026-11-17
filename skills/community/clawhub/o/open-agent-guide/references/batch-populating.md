# Batch populating

## Prerequisites

Install `bash`, `curl`, and `jq` for the shell scripts. Submission and watch
wrappers also require the [public `oag` CLI](cli.md#install-and-upgrade) and
Python 3.12 or newer. Use a shared `OAG_PACING_DIR` for concurrent CLI workers.
The shell validator has process-local pacing; coordinate it with other workers.

Request `guidance` alongside `status`, `resolution`, and `check_feedback` when
reading your submissions. An automated pipeline terminalizes each submission
within minutes, so watch it to terminal in the same session; no required human
review runs out of band. `guidance.next_action=wait` means keep watching to
terminal; `prepare_correction` means prepare the repair now but wait for
terminal closure before submitting it. `revise_and_resubmit` means inspect the
rejection, correct the proposal, then validate against the current catalog.
`none` means read the terminal resolution, including any successor links.
Guidance never reserves an identity or bypasses create conflicts. If it is
absent, keep using lifecycle status; never infer rejection from a check error.
Preserve submit/watch journals.

A merged submission completes its submission workflow. For a batch audit that
claims to check published values or filters, follow
[Check a published update](contributing.md#check-a-published-update) for each
product covered by the claim.

Seeding several catalog records in one pass — a new organization with nested
products and the full span of their relations (categories, jobs-to-be-done,
compliance certifications, agent skills, MCP servers, offers, referral programs,
developer kits, CLIs, and dimension-applicability declarations) — is more than
the single-record `curl` one-liners in [SKILL.md](../SKILL.md) cover. This
directory ships the three scripts a populator otherwise hand-rolls: a
`/validate/` dry-run, a paced submit pass, and a poller that renders each
submission's checks, reviews, and resolution.

Validation uses `bash`, `curl` and `jq`. Submit and watch require the installed
`oag` CLI, version 0.3.0 or newer. They provide durable journals, shared pacing,
and complete terminal evidence.

> A contract test (`test_skill_batch_reference.py` in the `submissions` app)
> round-trips the template below through the live API endpoints and asserts
> every JSON path these scripts read. If the API drifts, that test fails — so
> the scripts and this doc can't silently rot.

## Files

| File                                                                     | Role                                                                                                        |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| [`batch/org-with-product.batch.json`](batch/org-with-product.batch.json) | Payload template: two orgs — a hosted product and a self-hosted OSS one — spanning every relation envelope  |
| [`batch/oag-common.sh`](batch/oag-common.sh)                             | Shared helpers — auth, rate-limit pacing, 429 back-off. Sourced, not run                                    |
| [`batch/oag-validate-batch.sh`](batch/oag-validate-batch.sh)             | Dry-run every body against `POST /submissions/validate/`, then pre-flight every cited URL for 3xx redirects |
| [`batch/oag-submit-batch.sh`](batch/oag-submit-batch.sh)                 | Create each submission, capture the returned ids                                                            |
| [`batch/oag-watch.sh`](batch/oag-watch.sh)                               | Poll ids to a terminal state; render checks / reviews / resolution                                          |

## The batch file

A JSON array of submission bodies — the same shape you would `POST` to
`/submissions/` individually. Each body is
`{ app_label, model, submission_kind, description, payload }`.

An organization create needs three separate descriptions:

- `description` explains the proposed change and its evidence.
- `payload.description` describes the organization and is required even when the
  nested product has a description.
- `payload.products.create[].description` describes each product.

The JSON template includes all three. A missing organization description
produces an error naming `payload.description` and explaining the distinction.

The template ships **two** `catalog.organization` creates, each with one nested
product, together covering every relation envelope so you learn the shapes (not
a mandate to pack every field into a real first create — a nested org+product
create is all-or-nothing through fact-check, so one uncitable claim closes the
whole bundle and loses the org too; scope the create to what the pages you read
support and add the rest in per-source updates after merge; see contributing.md
→ "A nested org+product create is all-or-nothing through fact-check"). Within
that cited core, don't skip the citable fields either — those under-exercised
fields are the ones agents forget, and dropping ones you *could* cite is what
leaves records shallow (see contributing.md → "Draft for depth: fill every
decision-axis field you can cite"). The first org is a hosted product
(categories, compliance certs, jobs-to-be-done, agent skills, an MCP server,
offers, a referral program); the second is a self-hosted OSS product (a
developer kit, a CLI, and a dimension-applicability declaration). The payload
envelope is the part worth memorizing, because `/submissions/fields/` describes
each model in isolation but not how they nest:

```jsonc
"payload": {
  "name": "Example AI", "slug": "example-ai", "url": "…", "description": "…",
  "products": {                       // reverse FK (one-to-many): create | remove
    "create": [
      {
        "name": "Example Browser", "slug": "example-browser", "description": "…",
        "url": "…",                   // canonical homepage — NOT the docs portal
        "documentation_url": "…",     // docs home / developer-docs portal (the one docs front door)
        "categories":                 { "add": ["browser-automation"] },  // taxonomy: add | remove | propose
        "compliance_certifications":  { "add": ["soc-2"] },               // reference vocab: add | remove
        "capabilities": {             // proposable taxonomy: add an existing slug AND propose a new one inline
          "add": ["brand-asset-retrieval"],
          "propose": [ { "name": "Web Navigation", "slug": "web-navigation", "description": "…" } ]
        },
        "jobs_to_be_done": {          // proposable taxonomy: add an existing slug AND propose a new one inline
          "add": ["find-brand-assets"],
          "propose": [ { "name": "Automate a browser workflow", "slug": "automate-browser-workflow", "description": "…" } ]
        },
        "agent_skills":               { "propose": [ { "name": "…", "slug": "…", "url": "…" } ] }, // proposable; proposal requires a url
        "mcp_servers":                { "create": [ { "name": "…", "url": "…" } ] }, // nested reverse FK
        "referral_programs":          { "create": [ { "name": "…", "slug": "…", "program_url": "…", "status": "active" } ] },
        "offers":                     { "create": [ /* one per published plan */ ] }
      }
    ]
  }
}
```

The second org's product shows the dev-tooling and applicability envelopes:

```jsonc
"developer_kits": {                   // reverse FK; its own nested reference `add`s recurse
  "create": [ {
    "name": "…", "url": "…",
    "programming_languages": { "add": ["python", "typescript"] },  // reference vocab on the kit
    "licenses":              { "add": ["apache-2.0"] }              // license slug = SPDX id lowercased
  } ]
},
"command_line_interfaces": { "create": [ { "name": "…", "slug": "…", "url": "…" } ] },  // reverse FK
"dimension_applicability": [          // NOT an add/remove envelope — a per-dimension list, upsert by `dimension`
  { "dimension": "trust", "not_applicable": true, "justification": "…" }
]
```

Four envelope kinds show up, each with its own operations:

- **Reverse FK (one-to-many)** — `products`, `mcp_servers`, `api_specs`,
  `offers`, `referral_programs`, `developer_kits`, `command_line_interfaces`:
  `create` child objects (or `remove` by id). Nested creates recurse, so a
  product created under an org can itself carry `mcp_servers.create`, and a
  `developer_kits.create` child can itself carry `programming_languages.add` and
  `licenses.add`. **Model one `offer` per published pricing plan** (Free /
  Starter / Standard / Professional / Enterprise, …) rather than lumping the
  pricing page into a single offer — see SKILL.md → "Break pricing into one
  offer per plan".
- **Reference vocabulary (many-to-many)** — `compliance_certifications`,
  `licenses`, `programming_languages`, `access_controls`: `add` / `remove` an
  **existing** row. These are closed, staff-curated tables; you attach, you
  don't mint. A `License` slug is its SPDX id lowercased (`apache-2.0`).
- **Proposable taxonomy / vocab (many-to-many)** — `categories`, `capabilities`,
  `jobs_to_be_done`, `agent_skills`: `add` / `remove` an existing term, or
  `propose` a brand-new one inline (deduped against existing slugs, so a
  proposed slug that already exists just links the existing row). A taxonomy
  proposal takes `name` and an optional `slug`. Categories require a nonblank
  `description`; capabilities and jobs-to-be-done accept an optional
  description. Direct category creates also require `payload.description`,
  separately from the submission justification. An `agent_skills` proposal
  additionally **requires a `url`**. `jobs_to_be_done` is the catalog's
  most-neglected relation — propose one whenever a product serves a job no
  existing JTBD names.
- **Dimension applicability** — `dimension_applicability` is **not** an
  add/remove/create envelope but a list of per-dimension declarations, upserted
  by `dimension`. Mark a scoring dimension (`integration`, `trust`,
  `portability`, `security`) not-applicable with a required `justification` when
  it genuinely doesn't fit the product's category. A guardrail rejects any
  declaration that would leave fewer than two applicable dimensions or less than
  half the nominal scoring weight (ADR-0015).

**Reference existing objects by natural key, not UUID.** Every `add` / `remove`
entry and scalar foreign key accepts the object's `slug` directly (ADR-0020), so
you rarely need to enumerate a vocabulary table first — draft straight from the
slugs you already hold. `soc-2`, `browser-automation`, `apache-2.0`, `python`
above are slugs. (See SKILL.md → "Loading reference/vocabulary tables without
hitting the rate limit".)

Confirm the writable field set for any model before drafting:

```bash
curl -fsSL "$OAG_BASE_URL/api/v1/submissions/fields/?app_label=catalog&model=product&view=summary" \
  -H "Authorization: Bearer ${OAG_TOKEN}" | jq
```

## The loop: validate → submit → watch

```bash
export OAG_TOKEN=oag_...        # bearer token, see SKILL.md
# Optional: this is also the default for every batch script.
export OAG_BASE_URL=https://www.openagentguide.com
cd references/batch

# 1. Dry run. Catches payload-shape and natural-key errors before you create
#    anything, then pre-flights every pointer/affordance URL for 3xx redirects
#    (OAG_PREFLIGHT=0 skips the URL check for offline validation).
./oag-validate-batch.sh org-with-product.batch.json

# 2. Create. Paced under the mutation limit; writes new ids to submitted-ids.txt.
./oag-submit-batch.sh org-with-product.batch.json submitted-ids.txt

# 3. Watch to terminal. Renders per-check status, then the resolution reason.
./oag-watch.sh --file submitted-ids.txt
```

`oag-watch.sh` delegates to `oag watch`. With `--file IDS.txt`, it stores its
journal at `IDS.txt.watch.journal.json`; use `--journal PATH` to choose another
location. Positional IDs require `--journal PATH` or `OAG_WATCH_JOURNAL`. Resume
with the same IDs and journal to retain terminal evidence. The CLI emits results
at completion, including full check/review evidence and resolution for terminal
submissions. `OAG_WATCH_TIMEOUT` sets the deadline, default 900 seconds. The
wrapper returns CLI exit codes; 4 means pending and 3 means unresolved reads.
The old `OAG_READ_INTERVAL` and `OAG_WATCH_INTERVAL` settings no longer apply.

## URL redirect pre-flight

`oag-validate-batch.sh` ends by probing every bare-URL value in the batch — the
pointer fields (`url`, `documentation_url`, `source_code_url`, `pricing_url`,
`program_url`) and the nested affordance URLs (MCP servers, developer kits,
CLIs, agent skills) — with `curl` **without** `-L`, and fails the run on any
`3xx`. This catches the single highest-yield populator trap: the pipeline
fetcher does **not** follow redirects, so a path you "verified" with `curl -L`
that `301`s to a canonical path leaves the fetcher with a `404` body and closes
the submission on a URL you just saw working. The check prints the canonical
target (`%{redirect_url}`) for each redirecting URL — swap it into the payload
and re-validate. Set `OAG_PREFLIGHT=0` to skip the probe when validating
offline. Probing reads external URLs only and needs no token.

## Rate limits and pacing

Submission mutations are capped at **20 / minute + 5 / second burst**. A
validate + submit + resubmit loop over ten items brushes that ceiling, and one
accidental re-run of a submit pass will return `429` mid-batch. The scripts pace
automatically. The submit wrapper uses CLI pacing; these environment knobs apply
to the remaining shell scripts:

- `oag-common.sh` sleeps `OAG_MUTATION_PACE_SECONDS` (default **3.5s**) between
  mutating calls — ~17/min, under the 20/min ceiling with headroom.
- Each request has a timeout of `OAG_REQUEST_TIMEOUT` (default 45s).
- On a mutation `429` it waits and retries up to `OAG_MAX_ATTEMPTS` (default 5)
  — honoring `Retry-After` if present, else pausing `OAG_MUTATION_PACE_SECONDS`.
  Request throttles return `Retry-After` in seconds and `X-RateLimit-Scope`
  naming each exhausted shared-account budget. Pause all workers on that account
  for the indicated wait, then add jitter. The open-submission-cap `429` below
  is not transient and has no retry header.

Two more caps to know:

- **Open-submission cap: 25 per user.** `POST /submissions/` returns `429` once
  you have 25 open submissions awaiting review. Trusted populator accounts in
  the "Bulk submitters" group (the `submissions.bulk_submit_catalogsubmission`
  permission) are exempt — that is the intended way to seed a large batch in one
  pass.
- **Authenticated reads: 120 / minute / account.** All tokens for the same
  account share this budget. Submit and watch wrappers share CLI pacing when
  using the same origin, token, and `OAG_PACING_DIR` on one host.

For efficient polling, prefer
`oag watch --file submitted-ids.txt --journal watch.json` from oag-client
0.3.0+. It reads up to 100 pending IDs per request, fetches full terminal
evidence once, and reuses that evidence when resuming the journal. Custom
clients can use
`/api/v1/submissions/?ids=UUID,UUID&page_size=100&fields=id,status,review_ready,check_feedback,guidance`.
The server returns newest-first pages and omits missing IDs. Cache terminal
results and stop polling those IDs; request a fresh snapshot only when needed.

Failed reads remain unresolved and cannot report a successful watch. Terminal
snapshots include every checks and reviews page before they enter the cache.

## Recovering rejects

Submissions are immutable — you don't fix one, you submit a corrected new one
(SKILL.md → "After you submit"). For a batch:

- Read each `resolution.closed.reason` and the fact-check evidence from the
  watcher output, correct the offending body in the batch file, and re-run
  submit + watch on just those rows.
- Inspect `check_feedback` and `links.checks` before repair. Explain each
  substantive correction and prior submission ID in the new `description`.
  Compare old and new payloads: flag an identical rejected body as a blind
  repeat and stop that row. A changed key or description is not a correction.
  Seek review with evidence if the verdict seems wrong. Transient errored checks
  automatically retry with capped exponential backoff on the same open
  submission. Keep polling it; do not submit a duplicate for a timeout.
  Deterministic errors do not auto-retry, and persistent failures may need
  operator triage. Errored checks do not reject or close submissions. Ambiguous
  HTTP retries use the same key.
- A create wedged `open` by a review-side stall holds its slug; supersede it by
  re-posting with `"force": true` (SKILL.md → "Unwedging a slug").

## CLI coordination and batch budgets

The installed `oag` CLI provides validation, journaled submission, status, and
batched watch. See [the client guide](cli.md#pacing-and-workflow-deadlines) for
shared pacing, Retry-After handling, and sizing workflow deadlines against
combined throughput. `oag-submit-batch.sh` and `oag-watch.sh` delegate to that
CLI and participate in its shared pacing. The curl-based validation/preflight
script uses its own delays; it does not read `OAG_PACING_DIR` or share CLI
cooldowns. Coordinate it with other account activity yourself. Prefer CLI
validation and watch for concurrent work; retain the shell preflight when you
need external citation URL checks.

Allow time for other workers' reservations, retries, and terminal-evidence
fetches. Mutation reservations leave read slots unchanged; both lanes still
honor shared Retry-After cooldowns. Inspect `deadline_error` on unresolved watch
records when a budget expires. Pacing does not bound outstanding server work or
prevent every deadline failure. Resume the same submit journal after an
uncertain write and the same watch journal to retain terminal evidence.

### Transport failures during validation and submission

Validation retries curl transport failures, reported as HTTP `000`, and 5xx
responses up to `OAG_MAX_ATTEMPTS`. Exhausted requests print `UNRESOLVED` and
exit nonzero. They do not establish that a payload is invalid. Error bodies may
be HTML or empty; the script reports them without requiring JSON.

The shell submitter now delegates to `oag submit`. Install or upgrade to
**oag-client 0.2.0+** first. Its compatible invocation is:

```sh
./oag-submit-batch.sh batch.json ids.txt [submit.journal.json]
```

The default journal is `ids.txt.journal.json`. Keep it and the batch unchanged
on restart. The CLI persists one key per row and safely retries keyed
transport/5xx failures, including after restart. Confirmed rows are skipped and
their IDs remain in the output file. Existing nonempty ID files without a
journal are refused; older unkeyed journal rows still require `oag reconcile`.
Do not rerun an old unjournaled batch after an uncertain write, even if its ID
file is empty.

The wrapper prints the CLI JSON result, writes only confirmed IDs, and returns
CLI exit codes. `OAG_SUBMIT_TIMEOUT` controls its total budget, default 300
seconds. It uses CLI pacing and five-attempt retries; the shell transport's
`OAG_REQUEST_TIMEOUT`, `OAG_MUTATION_PACE_SECONDS` and `OAG_MAX_ATTEMPTS` apply
to the remaining shell scripts, not this wrapper.
