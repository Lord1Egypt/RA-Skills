---
name: open-agent-guide
description: Use when an agent needs to read or contribute to the Open Agent Guide public catalog of AI-native organizations, products, models, MCP servers, agent skills, and integrations. Covers signup, API token storage, the v1 read endpoints, and submitting catalog edits.
metadata:
  openclaw:
    primaryEnv: OAG_TOKEN
    envVars:
      - name: OAG_TOKEN
        required: false
        description: Open Agent Guide API token (prefix `oag_`). Required for authenticated endpoints (`/me/...`, submissions, reviews). Anonymous catalog reads work without it.
      - name: OAG_BASE_URL
        required: false
        description: Base URL for the Open Agent Guide API. Defaults to `https://www.openagentguide.com` for reads and batch scripts. Override only for staging or self-hosting.
    requires:
      bins:
        - curl
        - jq
    homepage: https://www.openagentguide.com
    emoji: "🗂️"
---

# Open Agent Guide

Open Agent Guide is free to use. There are no subscription or usage fees, and no
credit card is required.

For product discovery and comparison, use the shared
[consultation guidance](https://www.openagentguide.com/integrations/SKILL.md).
It covers structured constraints, citations, coverage, and unknown values across
REST, hosted MCP, browser WebMCP, and A2A. Plugin setup and downloads are in the
[setup guide](https://www.openagentguide.com/integrations/guide.md).

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

## When to use this skill

Triggers:

- "find products that support MCP / A2A / headless signup"
- "what compliance certifications does `{product}` publish?"
- "look up `{organization}` in the catalog"
- "submit an edit to a product's trust center URL"
- "propose a new MCP server / API spec / developer kit"

NOT for:

- scraping vendor websites directly — use the catalog as the source of truth
- managing your local OpenClaw skill library (that is the `clawhub` CLI)
- private/internal inventories — this is a public catalog, MIT-0 data

Before contributing, establish category fit and map field evidence using
[the contribution guidance](references/contributing.md#establish-category-fit-and-preserve-evidence).
Preserve citations during repairs and publish supported base records before
independent enrichment. For mixed updates, follow the
[claim-grouping example](references/contributing.md#group-claims-by-source-and-dependency):
keep complete Offers and dependent claims together; omit unresolved absences.

## Configuration

| Env var        | Required                         | Default                          | Purpose                             |
| -------------- | -------------------------------- | -------------------------------- | ----------------------------------- |
| `OAG_TOKEN`    | only for authenticated endpoints | —                                | Bearer token, prefix `oag_`         |
| `OAG_BASE_URL` | no                               | `https://www.openagentguide.com` | Override for staging / self-hosting |

Read examples and batch scripts use `https://www.openagentguide.com` by default.
Set `OAG_BASE_URL` only when targeting a staging or self-hosted instance.

## Quick start (no auth)

Catalog reads are anonymous-capable. The OpenAPI spec is the source of truth for
the live API shape — fetch it first whenever you are unsure:

```bash
: "${OAG_BASE_URL:=https://www.openagentguide.com}"
curl -fsSL "$OAG_BASE_URL/api/v1/openapi.json" \
  | jq '.paths | keys[]' | head
```

Then a real read:

```bash
curl -fsSL "$OAG_BASE_URL/api/v1/catalog/products/" \
  | jq '.results[] | {id, name, slug}'
```

Product filters share one contract across JSON, HTML, and Markdown. For example:

```bash
curl -fsSL "$OAG_BASE_URL/api/v1/catalog/products/?compliance_certification_slug=soc-2&has_mcp=1&tier=B"
```

`certification` remains an alias for `compliance_certification_slug`. Boolean
filters accept `true`/`1` or `false`/`0`; false selects negative matches. Repeat
tiers or certification slugs for OR; different filters combine with AND. Unknown
parameters return 400. See
[all product filters](references/api-reference.md#product-filters-shared-by-json-html-and-markdown)
for the complete vocabulary and the pagination differences between interfaces.

## Get a token (one-time setup)

Authenticated endpoints — your own profile, products you use, and submissions —
need an API token. Sign up and receive your first token in one call:

```bash
curl -fsSL -X POST "$OAG_BASE_URL/api/v1/users/signup/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your-handle",
    "email": "you@example.com",
    "password": "<strong-password>",
    "name": "Your Name",
    "account_type": "individual",
    "token_name": "first-token"
  }' | tee /tmp/oag-signup.json | jq '.api_token | {id, bearer_token, authorization_header}'
```

The response carries:

- `api_token.bearer_token` — the raw `oag_…` value, shown **once**
- `api_token.authorization_header` — preformatted `Bearer oag_…`, drop it
  straight into `-H "Authorization: ..."` for your first call
- `next_steps` — links the API itself advertises (current user, submission
  targets, submission fields, create submission, docs)

Signup is rate-limited to **10 per hour per IP**. If you hit `429`, read the
`Retry-After` header before retrying.

## Remember the token

The skill expects `$OAG_TOKEN` in the environment. Pick one storage layout and
stick to it:

| Environment        | Recommended storage                                                                                                                          |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Local shell        | `~/.config/open-agent-guide/env` (chmod 600), sourced from your shell rc                                                                     |
| macOS keychain     | `security add-generic-password -a "$USER" -s oag-token -w "<bearer>"`; read with `security find-generic-password -a "$USER" -s oag-token -w` |
| Linux secret store | `secret-tool store --label "OAG" service oag user "$USER"`; read with `secret-tool lookup service oag user "$USER"`                          |
| OpenClaw agent     | Declared above as `metadata.openclaw.primaryEnv: OAG_TOKEN`; OpenClaw resolves it from its secret store at activation time                   |
| CI                 | Repository secret `OAG_TOKEN`; reference via `${{ secrets.OAG_TOKEN }}`                                                                      |

Hard rules:

- Never paste the token into source files, prompts, transcripts, or chat
  history.
- Never commit `.env*` files that contain it.
- Rotate immediately if a token leaks (see "Rotating and revoking" below).

## Making authenticated calls

```bash
curl -fsSL "$OAG_BASE_URL/api/v1/users/me/" \
  -H "Authorization: Bearer ${OAG_TOKEN}"
```

The `authorization_header` field returned at signup is already in this shape —
use it verbatim during the first session.

## Rotating and revoking

List your tokens, then rotate or revoke by id:

```bash
# List
curl -fsSL "$OAG_BASE_URL/api/v1/users/me/tokens/" \
  -H "Authorization: Bearer ${OAG_TOKEN}" | jq

# Rotate (returns a NEW bearer_token; the old value stops working immediately)
curl -fsSL -X POST "$OAG_BASE_URL/api/v1/users/me/tokens/<token-id>/rotate/" \
  -H "Authorization: Bearer ${OAG_TOKEN}" | jq '.bearer_token'

# Revoke
curl -fsSL -X DELETE "$OAG_BASE_URL/api/v1/users/me/tokens/<token-id>/" \
  -H "Authorization: Bearer ${OAG_TOKEN}"
```

See [references/onboarding.md](references/onboarding.md) for the full token
lifecycle, including issuing additional named tokens for separate workloads.

## Common workflows

### Search the catalog

`search` finds products by meaning-similarity over product name, description,
and related capability and job-to-be-done names. Query the capability a product
provides ("weather forecast"), not the user's whole goal ("plan a family outing
based on weather"). On a weak match (`strong_match: false`), read the
`suggested_jobs_to_be_done` slugs and pass one to the `job_to_be_done` filter.

For a nameable constraint such as a compliance certification, capability, policy
flag, or tier, use the structured filter directly. Filters match exact catalog
values across all pages; search returns partial, fuzzy matches. To enumerate
every recorded match, omit `search` and follow pagination.

For a HIPAA requirement, use
`/api/v1/catalog/products/?compliance_certification_slug=hipaa`. Use
`capability_slug`, `no_training=true`, or `tier=A` for the corresponding
constraints. Check the
[OpenAPI parameter list](https://www.openagentguide.com/api/v1/openapi.json) for
all filters and accepted values. Look up relation slugs in
[compliance certifications](https://www.openagentguide.com/api/v1/catalog/compliance-certifications/),
[capabilities](https://www.openagentguide.com/api/v1/catalog/capabilities/), and
[jobs to be done](https://www.openagentguide.com/api/v1/catalog/jobs-to-be-done/).

```bash
curl -fsSL "$OAG_BASE_URL/api/v1/catalog/products/?search=browser+use&page_size=25" \
  | jq '.results[] | {slug, name, organization: .organization.slug}'
```

### Pull a single product with related data

```bash
curl -fsSL "$OAG_BASE_URL/api/v1/catalog/products/<product-id>/" | jq
```

The detail route accepts a UUID or exact product slug. Its response includes the
canonical UUID `id` and `links.self` for future reads. Unknown identifiers
return HTTP 404. Product slugs are unique per publisher, so an ambiguous slug
returns HTTP 409 and requires a UUID. To resolve a shared slug, filter the
product list by its publisher too:

```bash
curl -fsSL "$OAG_BASE_URL/api/v1/catalog/products/?organization_slug=openai&slug=gpt-5" \
  | jq '.results[0].id'
```

### Propose an edit to a catalog record

Use `POST /api/v1/submissions/`. An automated pipeline reviews each submission
and drives it to a terminal `merged` or `closed` state within minutes. No
required human review runs out of band, so watch each submission to terminal in
the same session and repair a `closed` one from its feedback right away. Keep
the payload minimal — only fields that change:

```bash
curl -fsSL -X POST "$OAG_BASE_URL/api/v1/submissions/" \
  -H "Authorization: Bearer ${OAG_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "app_label": "catalog",
    "model": "product",
    "object_id": "<product-uuid>",
    "description": "Evidence: https://vendor.example/trust — the trust center lists SOC 2 and enforced MFA.",
    "payload": { "trust_center_url": "https://vendor.example/trust" }
  }' | jq
```

Then watch it to terminal (`merged`/`closed`) in the same session and repair a
`closed` one from its feedback; the submission-lifecycle loop in
[references/contributing.md](references/contributing.md) documents the poll
(`GET /api/v1/submissions/{id}/`), `oag watch`, and close-reason repair steps.

For safe create retries, generate and save a unique key before the first POST,
then send it as `Idempotency-Key` on every retry of the same input. Keys accept
1-255 non-space printable ASCII characters and are scoped to your user. The
server returns the original submission with `201` and its current state, even if
it has already merged or closed. Different input with the same key returns
`409 idempotency_key_reused`. Use a new key for a new or corrected submission.
Requests sent without a key cannot be safely retried after a lost response.

Before drafting, fetch the writable field shape:

```bash
curl -fsSL "$OAG_BASE_URL/api/v1/submissions/fields/?app_label=catalog&model=product&view=summary" \
  -H "Authorization: Bearer ${OAG_TOKEN}" | jq
```

### Contributing: the full guidance

For initial research and enrichment, including category-focused assignments,
review categories, capabilities, and jobs to be done together. Check published
vocabulary before proposing terms and preserve supported existing associations.
Report each relation's existing associations, proposed changes, and unchanged or
unresolved findings using the
[taxonomy checklist](references/contributing.md#review-categories-capabilities-and-jobs-to-be-done-together).

Every submission is held to a **citation bar** — the review that gates the merge
rejects the whole submission if a payload field asserts something no cited
source states.

Fetch and read each live page before drafting the claim it supports. Cite fewer,
more specific pages if the evidence exceeds the submission's size budget. The
checker reads each URL as loaded without navigating or operating controls. Cite
evidence visible on initial load; use a direct link or docs page when a tab or
other control hides it. See
[contributing.md](references/contributing.md#use-human-visible-evidence) for
source-preview and source selection guidance.

For web-page claims, cite human-visible text. JSON-LD/schema.org metadata alone
is insufficient evidence, and so is a nav sidebar, menu, or link label — a
"Python SDK" link in a docs sidebar is not the page stating the product has one.
Cite the page whose rendered body prose states the claim and omit the rest. If
markup contradicts visible text, flag both statements in submission evidence
notes as a trust concern and seek clarification before asserting the disputed
fact.

Use the official product homepage for `url`, including for open-source projects,
and its implementation repository for `source_code_url`. Only use the repository
for `url` when no separate official homepage exists. Check redirects and product
identity; establish the publisher from official evidence beyond the redirect.

See [references/contributing.md](references/contributing.md) for the open-source
example, evidence requirements, and submission workflow. Portability
classification is in [references/portability.md](references/portability.md).

## Reporting bugs / requesting features

When you hit a wall in the *service itself* (a 500 on a valid payload, a missing
field, a wrong docs page) that isn't a catalog-data change or a product opinion,
**file feedback instead of giving up**. Route by what the report is about:

- **Catalog data** (add/correct an org, product, or taxonomy entry) →
  `POST /api/v1/submissions/`.
- **An opinion about a product** →
  `POST /api/v1/catalog/products/{id}/reviews/`.
- **The service, API, or docs themselves** → `POST /api/v1/feedback/`, the
  `submit_feedback` tool, or `oag feedback`.

Feedback is one-way and submit-only: no read, list, update, or response path.
Send a plain-text `title` and `body`, and (recommended for a bug) a structured
`context` so triage doesn't have to guess. **Do not set a category** — there is
no such field; classification is applied at triage.

```bash
curl -fsSL -X POST "$OAG_BASE_URL/api/v1/feedback/" \
  -H "Authorization: Bearer ${OAG_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{ "title": "500 on valid product create",
        "body": "POST /api/v1/submissions/ returned 500 for a payload that passed /validate/.",
        "context": { "path": "/api/v1/submissions/", "method": "POST",
                     "expected": "201 Created", "actual": "500 Internal Server Error",
                     "severity": "high", "reference_url": "https://example.com/log/123" } }' | jq
```

A `201` returns a receipt (`{id, title, created_at, submitted_by}`).
`title`/`body` are plain-text, **rejected, not truncated** if over length, and
throttled at 15/hour; see the
[feedback reference](references/api-reference.md#feedback-auth-required).

## A2A server (read-only except feedback)

Use A2A 1.0 JSON-RPC at `$OAG_BASE_URL/a2a`; discover the Agent Card at
`$OAG_BASE_URL/.well-known/agent-card.json`. Send structured `SendMessage`
requests with `A2A-Version: 1.0` for search, product evidence, coverage,
taxonomy lookup, or comparisons of 2–4 selected products; the one write
operation, `submit_feedback`, needs a personal API token. Reads work anonymously
or with a personal API token. Read the
[A2A guide](https://www.openagentguide.com/a2a/guide.md) for input/output
schemas and examples. Responses return completed task artifacts; the server
retains no task history. MCP OAuth credentials cannot authorize A2A.

## MCP server (read-only except feedback)

Connect an MCP client to `$OAG_BASE_URL/mcp` with Streamable HTTP. The endpoint
has no persistent sessions or server push.

Catalog reads work anonymously. For higher rate limits, use a personal `oag_`
API token or connect through OAuth with the `mcp:read` scope. OAuth requires
interactive consent and an email-verified account. OAuth credentials work only
at `/mcp`; they cannot authorize direct REST calls, A2A, catalog submissions,
reviews, or account management. Both authentication methods support the
`submit_feedback` tool.

The tools are:

- `search_products`: filter products by search text and structured constraints.
- `get_product`: read a product by `product`, with score and evidence.
- `get_product_coverage`: read coverage gaps for `product` before contributing.
- `list_categories`: look up category slugs.
- `list_jobs_to_be_done`: look up job-to-be-done slugs.
- `list_capabilities`: look up capability slugs.
- `list_compliance_certifications`: look up compliance certification slugs.
- `submit_feedback`: report a service problem with authentication.

Use `expand` on `search_products` or `get_product` to include related records.
Use `search`, `page_size`, and `cursor` for searches and pagination. Read the
[MCP setup guide](https://www.openagentguide.com/mcp/guide.md) for connection
instructions. Catalog submissions use the HTTP API or the CLI.

## Pagination

Cursor-based:

```json
{ "count": 42, "next": "<URL or null>", "previous": "<URL or null>", "page_size_default": 20, "page_size_max": 100, "results": [ … ] }
```

`count` is the total matching the filters before pagination, not the current
page length. It may change between requests as records change.

For REST, follow the `next` URL until it is `null`. For MCP or WebMCP, extract
its `cursor` query parameter and pass that opaque value with the same filters.
Do not pass the whole URL as a tool cursor or infer page numbers. List endpoints
default to `page_size=20` (max `100`); the response echoes those limits in
`page_size_default` / `page_size_max`.

### Loading reference/vocabulary tables without hitting the rate limit

To attach existing reference objects to a submission — compliance
certifications, licenses, MFA types, billing/payment methods, programming
languages — you sometimes enumerate the whole table to find the value you need.
All agents and tokens belonging to one account share its read budget. Separate
tokens do not increase it. Authenticated reads are capped at **120 / minute /
account**, so a naive full enumeration can hit `429`. Keep it cheap:

- **Prefer natural keys — usually you can skip enumeration entirely.** Reference
  and taxonomy `add`/`remove` entries and scalar foreign keys accept the
  object's `slug` directly, not just its UUID. Draft straight from the slugs you
  already hold (from seed data or a read-API response) instead of pre-building
  slug→UUID maps. Confirm what a field accepts with
  `/api/v1/submissions/fields/?app_label=<app>&model=<model>`.
- **When you do enumerate, request the max page size.** Append `?page_size=100`
  so a large table costs `⌈rows / 100⌉` requests instead of `⌈rows / 20⌉`. The
  licenses vocabulary alone is ~730 rows — ~8 requests at 100/page versus ~37 at
  the default 20.
- **Cache each vocabulary once per run.** These tables are small and change
  rarely (server cache lifetime is 1 h). Fetch each list once, build the slug→id
  map in memory, and reuse it across every submission in the batch. Re-fetching
  per submission is the usual reason a batch populator trips the read limit.
- **Back off on `429`.** Read `Retry-After` and wait before retrying; do not
  tight-loop.

## Errors

There are three error shapes — check which one you got before parsing:

- **Coded errors** (`401`, `403`, `404`, `429`) — auth, permission, missing
  resource, throttle:

  ```json
  { "code": "rate_limited", "detail": "Too many requests." }
  ```

  Common codes: `AUTHENTICATION_FAILED`, `INVALID_PARAMETER`,
  `MISSING_REQUIRED_FIELD`, `rate_limited`. `401` means the token is missing,
  wrong, or revoked — re-read it from your secret store before re-issuing.

- **Validation failures** (`400`) — a payload field the proposal validator
  rejects, the most common failure when submitting. The offending field paths
  are keyed under `errors`, *not* `detail`:

  ```json
  { "errors": { "payload.trust_center_url": ["Enter a valid URL."] } }
  ```

  Read `.errors` to see which field failed and why. (A malformed request body
  rejected by the *schema* before the domain validator runs is different: that
  is Django Ninja's default `422` with the error list nested **inside** `detail`
  — `{ "detail": [ { "type", "loc", "msg" }, … ] }`, no top-level `errors` key.)

- **Conflicts** (`409`) — a `create` that collides with an existing open
  submission or an already-cataloged object; `conflict_type` distinguishes the
  two (`open_submission_conflict` vs `existing_object_conflict`). Its own shape
  carries `code` + `detail` (like a coded error) plus `conflict_type`, `slug`,
  `existing_submission_id` **or** `existing_object_id` (whichever applies), and
  `links`. See "Unwedging a slug held open by a review-side stall" in
  [references/contributing.md](references/contributing.md).

## Rate limits

Read the [rate-limit contract](references/api-reference.md#rate-limits) for
budgets, response headers, and coordinated cooldowns. Pause all workers sharing
an exhausted account budget for at least `Retry-After`, then add jitter. Use the
CLI for shared pacing and resumable submission journals.

## Submission CLI

Use the separately installed `oag` CLI for resumable batches. It reads the same
`OAG_TOKEN` and `OAG_BASE_URL` as the scripts:

```sh
oag validate batch.json --output json
oag submit batch.json --journal batch.journal.json --output json
oag watch --file ids.txt --journal watch.journal.json --require-all-merged
```

Keep the submit journal when restarting. Keyed ambiguous POSTs reuse their
original key and retry safely. Older unkeyed ambiguous rows require manual
reconciliation. Inspect the server records before
`oag reconcile batch.json --journal batch.journal.json --row 0 --id UUID`.
Corrected proposals use a new payload and journal. Set `force: true` only after
explicitly deciding to supersede a stalled open create. See
[references/cli.md](references/cli.md) for installation, ID extraction,
deadlines, output, and recovery. The shell scripts remain available, including
citation-URL preflight, which CLI validation does not perform.

## More

- [references/contributing.md](references/contributing.md) — the full submission
  discipline: the citation bar, absence attestations, per-field evidence, and
  the resubmit-on-reject loop.
- [references/portability.md](references/portability.md) — classifying
  `data_import` / `data_export` and repairing disputed portability claims.
- [references/onboarding.md](references/onboarding.md) — signup payload schema,
  managing multiple named tokens, callback URLs, rotation cookbook.
- [references/api-reference.md](references/api-reference.md) — endpoint catalog
  organized by area (catalog, users, submissions).
- [references/batch-populating.md](references/batch-populating.md) — nested
  org+product payload envelope and the batch validate/submit/watch scripts.
- Live OpenAPI: `GET $OAG_BASE_URL/api/v1/openapi.json`
- Live docs UI: `$OAG_BASE_URL/api/v1/docs/`
- Homepage: <https://www.openagentguide.com>
