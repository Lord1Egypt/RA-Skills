# API reference

Endpoint catalog for the Open Agent Guide public API, organized by area. The
**live OpenAPI spec at `$OAG_BASE_URL/api/v1/openapi.json` is authoritative** —
this file is a hand-curated map for orientation. Default base is
`https://www.openagentguide.com`. All paths below assume the `/api/v1` prefix.

## Authentication

`Authorization: Bearer <oag_…>` — see SKILL.md and `onboarding.md`. Catalog read
endpoints accept anonymous requests; everything under `/users/me/` and
`/submissions/` requires a token.

## Catalog (anonymous-capable)

Discovery endpoints over the public AI-ecosystem catalog.

### Core

| Method | Path                                                  | Purpose                        |
| ------ | ----------------------------------------------------- | ------------------------------ |
| GET    | `/catalog/organizations/`                             | List organizations             |
| GET    | `/catalog/organizations/{organization_id}/`           | Retrieve organization          |
| GET    | `/catalog/products/`                                  | List products                  |
| GET    | `/catalog/products/{product_id}/`                     | Retrieve product               |
| GET    | `/catalog/products/{product_id}/reviews/`             | Public reviews for a product   |
| POST   | `/catalog/products/{product_id}/reviews/`             | Submit a product review (auth) |
| DELETE | `/catalog/products/{product_id}/reviews/{review_id}/` | Delete own review (auth)       |
| GET    | `/catalog/people/`                                    | List people                    |
| GET    | `/catalog/people/{person_id}/`                        | Retrieve person                |

### Product filters shared by JSON, HTML, and Markdown

Use `search` for fuzzy capability discovery, such as "browser use" matching
"Browser Automation". Its semantic recall uses product name, description, and
related capability and job-to-be-done names; it does not translate a query into
structured filters. For a nameable constraint such as a compliance
certification, capability, policy flag, or tier, use the structured filter
directly. Filters match exact catalog values across all pages; search returns
partial, fuzzy matches. To enumerate every recorded match, omit `search` and
follow pagination.

For a HIPAA requirement, use
`/api/v1/catalog/products/?compliance_certification_slug=hipaa`. Use
`capability_slug`, `no_training=true`, or `tier=A` for the corresponding
constraints. Check the
[OpenAPI parameter list](https://www.openagentguide.com/api/v1/openapi.json) for
all filters and accepted values. Look up relation slugs in
[compliance certifications](https://www.openagentguide.com/api/v1/catalog/compliance-certifications/),
[capabilities](https://www.openagentguide.com/api/v1/catalog/capabilities/), and
[jobs to be done](https://www.openagentguide.com/api/v1/catalog/jobs-to-be-done/).

`no_training` filters protection of non-public data from generative AI training,
including foundation models. Predictive recommendation training and training
exclusively on public data fall outside the field. Positive matches include
conditional policies; inspect `no_training_on_user_data` and its cited policy
for the distinction between `yes` and `available`.

Use the same product filters on `/api/v1/catalog/products/`, `/products/`, and
`/products.md`. For example:
`/api/v1/catalog/products/?compliance_certification_slug=soc-2&has_mcp=1&tier=B`.
Replace the path with `/products.md` for the same filter in Markdown.

The canonical name for each publisher and taxonomy filter is the `*_slug` form.
The list also accepts the shorter names the MCP `search_products` tool uses
(`category`, `capability`, `job_to_be_done`, and `organization`) as documented
aliases, so the same word filters both surfaces. A canonical name and its alias
combine into one OR group.

| Parameters                                                                                                     | Meaning                                                                                                                   |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `search`                                                                                                       | Free-text product discovery                                                                                               |
| `organization_id`, `organization_slug`, `person_id`, `person_slug`                                             | Exact publisher membership; `organization` aliases `organization_slug`                                                    |
| `slug`                                                                                                         | Exact product slug (unique per publisher; pair with a publisher filter to resolve one product and its id)                 |
| `category_id`, `category_slug`, `capability_id`, `capability_slug`, `job_to_be_done_id`, `job_to_be_done_slug` | Exact taxonomy membership; `category`, `capability`, and `job_to_be_done` alias the slug filters                          |
| `compliance_certification_id`, `compliance_certification_slug`                                                 | Linked compliance certification; `certification` aliases `compliance_certification_slug`                                  |
| `access_control_id`, `access_control_slug`, `agent_skill_id`, `agent_skill_slug`                               | Linked access control or agent skill                                                                                      |
| `license_id`, `license_slug`, `benchmark_id`, `benchmark_slug`                                                 | Linked license or benchmark                                                                                               |
| `documentation_resource_id`, `documentation_resource_slug`, `mfa_type_id`, `mfa_type_slug`                     | Linked documentation or MFA type                                                                                          |
| `has_mcp`, `has_a2a`, `has_cli`, `has_api_spec`, `has_sdk`                                                     | Presence of a cataloged server, CLI, API specification, or developer kit                                                  |
| `has_mcp_url`                                                                                                  | Refines `has_mcp` to MCP servers with a dialable endpoint url; excludes documentation-only servers                        |
| `spec_type`                                                                                                    | API specification type: `openapi`, `grpc`, or `graphql`; repeat for OR                                                    |
| `sdk_language`                                                                                                 | Programming-language slug of a product's SDK (developer kit), e.g. `python`; repeat for OR                                |
| `headless_signup`, `web_mcp`, `open_standards`, `self_hostable`, `open_source`                                 | Known boolean product attributes                                                                                          |
| `data_export`                                                                                                  | Recorded export support: `full`, `partial`, or `none`; repeat for OR; excludes unknown                                    |
| `zero_data_retention`, `no_training`, `sandbox`                                                                | Policy support: positive matches `yes` or `available`; negative matches `no`                                              |
| `free_plan`, `pay_go`                                                                                          | Presence of an active Offer with a structured `price_kind: free` or `price_kind: usage` option                            |
| `billing_model`, `payment_method`                                                                              | Slug membership on active offers                                                                                          |
| `tier`                                                                                                         | AI-native score tier: `S`, `A`, `B`, `C`, or `D`; unscored products do not match                                          |
| `completion_support`, `route_kind`, `on_behalf_of`, `execution_human_requirement`                              | Completion facets matching one record together; optional job scope; blank leaves the facet unfiltered.                    |
| `documented_complete_for_job`, `finishes_without_human_for_job`                                                | Documented task completion predicates; each needs a `job_to_be_done` scope and excludes unknown (ADR-0124)                |
| `completes_job_via`                                                                                            | Callable interface kinds that complete the scoped job; repeat for OR; needs a `job_to_be_done` scope and excludes unknown |

Completion predicates match records that deliver the linked job's main outcome
by and large. Scope can limit cases or prerequisites while preserving that
outcome. Expand `documented_task_completions` to read the assessed route, scope,
conditions, human steps and delegation policy. `completes_job_via` selects
products that finish the scoped job through any one of the supplied callable
interface kinds (`api`, `mcp`, `a2a`, `cli`, `sdk`, `webmcp`, `agent_skill`,
`native_connector`; `web` and `prose` are not callable and are rejected). It
matches the route recorded for the assessed completion, not mere presence of the
interface, and asserts neither route eligibility nor delegated authority; a
`mcp` match does not imply a dialable endpoint, so add `has_mcp_url` for that.

`free_plan=true` matches products with an active Offer containing a structured
pricing option with `price_kind: free`. `free_plan=false` selects products with
no such recorded offer; it does not prove that the vendor has no free access.
Omitting `free_plan` leaves free access unfiltered. Prose-only free allowances
and trials do not match unless an active Offer has a qualifying structured
option. Matched offers can have quotas, eligibility restrictions, noncommercial
terms, or attribution requirements.

`free_plan` is also a readable field on each product (list and detail JSON, and
the Markdown product list), so you can rank a shortlist by cost without opening
each product. It reads back the filter: `true` when the product has an active
free-tier offer, `null` when none is recorded. It is never `false` — a missing
free offer is unresearched, not a confirmed "no free tier". Select it with
`fields=free_plan`.

For example, request `/api/v1/catalog/products/?free_plan=true&expand=offers`.
Inspect the expanded offers' `lifecycle_status` and `pricing_options` to locate
the qualifying option, then read `description`, `price_description`, and the
terms at `url` to check whether the free access suits the workload. Expansion
includes the product's offers, so inspect each offer independently.

Boolean filters accept `true`/`1` and `false`/`0`, with `yes`/`no` and
`on`/`off` as compatibility aliases. Letter case is ignored. Omit a filter to
leave it unconstrained. False means a negative match, not "disable this filter".
Unknown boolean/policy values match neither side. Absence of a cataloged
integration or offer is a catalog fact, not evidence that the vendor cannot
provide it. `has_mcp` tests server records, independently of the in-browser
`web_mcp` attribute.

Repeat any ID/slug membership filter, `spec_type`, `tier`, `billing_model`, or
`payment_method` for OR matching within that filter. Certification values under
either name belong to one OR group. Different filters combine with AND. Boolean
filters, `search`, and `following` accept one value; repetitions return HTTP 400
rather than silently selecting one. IDs are UUIDs; slugs match exactly.
Unmatched valid values return zero results. Empty capability/job dropdown values
mean no filter.

Unknown parameter names, invalid boolean/tier/spec_type values, and repeated
single-value filters return HTTP 400. JSON errors use `invalid_parameter`; web
errors are plain text. Malformed UUIDs retain JSON's HTTP 422 validation and
return HTTP 400 on web pages. These rules also apply when using
`Accept: text/markdown`.

`following` is a separate authenticated-user scope: use `following=true` or
another positive boolean spelling. False or invalid values return HTTP 400 on
both interfaces. Pagination and result presentation remain interface-specific:
JSON uses `page_size`, `cursor`, `fields`, and `expand`; web pages use `page`
and `sort` with `relevance`, `score`, or `name`. The JSON product payload's
`connect` object resolves the connect strings inline: the MCP endpoint URL, the
API `spec_type` and spec URL, and each SDK's language slugs, so you can start a
client without an `expand` round-trip. JSON includes person-published products;
the web product list currently includes only organization-published products.
The shared filters do not change that listing scope. MCP/A2A presence does not
establish delegation/autonomy; the catalog has no dedicated field for that.

### Taxonomy

| Method | Path                                     | Purpose                 |
| ------ | ---------------------------------------- | ----------------------- |
| GET    | `/catalog/categories/`                   | List categories         |
| GET    | `/catalog/categories/{category_id}/`     | Retrieve category       |
| GET    | `/catalog/capabilities/`                 | List capabilities       |
| GET    | `/catalog/capabilities/{capability_id}/` | Retrieve capability     |
| GET    | `/catalog/jobs-to-be-done/`              | List jobs-to-be-done    |
| GET    | `/catalog/jobs-to-be-done/{jtbd_id}/`    | Retrieve job-to-be-done |

### Reference data

| Method | Path                                  | Purpose                                 |
| ------ | ------------------------------------- | --------------------------------------- |
| GET    | `/catalog/licenses/`                  | Software licenses                       |
| GET    | `/catalog/compliance-certifications/` | SOC2, ISO, HIPAA, …                     |
| GET    | `/catalog/mfa-types/`                 | MFA mechanisms                          |
| GET    | `/catalog/payment-methods/`           | Accepted payment methods                |
| GET    | `/catalog/billing-models/`            | Billing models (subscription, usage, …) |
| GET    | `/catalog/benchmarks/`                | Benchmark records                       |
| GET    | `/catalog/documentation/`             | Documentation entries                   |
| GET    | `/catalog/access-controls/`           | Access-control mechanisms               |
| GET    | `/catalog/agent-skills/`              | Agent-skill records in the catalog      |
| GET    | `/catalog/programming-languages/`     | Programming languages                   |

(All reference endpoints also expose `/{id}/` for detail views.)

### Integrations

| Method | Path                                | Purpose                        |
| ------ | ----------------------------------- | ------------------------------ |
| GET    | `/catalog/api-specs/`               | Public API specifications      |
| GET    | `/catalog/a2a-servers/`             | Agent-to-agent servers         |
| GET    | `/catalog/mcp-servers/`             | Model Context Protocol servers |
| GET    | `/catalog/plugins/`                 | Plugin integrations            |
| GET    | `/catalog/native-connectors/`       | Native connector integrations  |
| GET    | `/catalog/command-line-interfaces/` | Vendor CLIs                    |
| GET    | `/catalog/developer-kits/`          | SDKs and developer kits        |

## Users (auth required, except signup)

| Method | Path                                  | Purpose                                                      |
| ------ | ------------------------------------- | ------------------------------------------------------------ |
| POST   | `/users/signup/`                      | Register an account and mint the first token (anon, 10/h/IP) |
| GET    | `/users/me/`                          | Current user profile                                         |
| GET    | `/users/me/tokens/`                   | List API tokens                                              |
| POST   | `/users/me/tokens/`                   | Issue a new named token                                      |
| GET    | `/users/me/tokens/{token_id}/`        | Retrieve token metadata                                      |
| PATCH  | `/users/me/tokens/{token_id}/`        | Rename or update callback URL                                |
| POST   | `/users/me/tokens/{token_id}/rotate/` | Rotate; returns a new bearer                                 |
| DELETE | `/users/me/tokens/{token_id}/`        | Revoke                                                       |
| GET    | `/users/me/bookmarks/`                | Products you've bookmarked                                   |
| POST   | `/users/me/bookmarks/`                | Bookmark a product                                           |
| GET    | `/users/me/bookmarks/{bookmark_id}/`  | Retrieve a bookmark                                          |
| PATCH  | `/users/me/bookmarks/{bookmark_id}/`  | Edit notes, jobs-to-be-done, follow flag                     |
| DELETE | `/users/me/bookmarks/{bookmark_id}/`  | Remove                                                       |

## Submissions (auth required)

The submissions surface is how external agents propose changes to the catalog.
All submission writes are reviewed before merging.

### Discovery

| Method | Path                                                  | Purpose                                                                                     |
| ------ | ----------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| GET    | `/submissions/targets/`                               | Models you may submit against (app_label, model, capabilities)                              |
| GET    | `/submissions/fields/?app_label=&model=&view=summary` | Writable field schema for one target. `view=summary` is the compact agent-friendly response |

Always call `/submissions/fields/` before drafting a payload — the writable set
is narrower than the read schema and changes as the catalog evolves.

### Listing and inspection

| Method | Path                                    | Purpose                                                                         |
| ------ | --------------------------------------- | ------------------------------------------------------------------------------- |
| GET    | `/submissions/`                         | List submissions (filters: `status`, `app_label`, `model`, `slug`, `object_id`) |
| GET    | `/submissions/{submission_id}/`         | Submission detail                                                               |
| GET    | `/submissions/{submission_id}/reviews/` | Reviewer comments                                                               |
| GET    | `/submissions/{submission_id}/checks/`  | Async validation results                                                        |
| GET    | `/submissions/{submission_id}/events/`  | Lifecycle event log                                                             |

A transient `errored` check keeps the same submission `open` while the service
automatically retries with capped exponential backoff. Keep polling that
submission; do not create a duplicate to work around a timeout. Deterministic
errors do not auto-retry, and persistent failures may need operator triage. An
errored check does not reject or close the submission. For a `closed`
submission, read the reason and repair the rejected content before resubmitting.

### Mutation

| Method | Path                                                        | Purpose                                           |
| ------ | ----------------------------------------------------------- | ------------------------------------------------- |
| POST   | `/submissions/validate/`                                    | Preflight a payload without creating a submission |
| POST   | `/submissions/`                                             | Create a submission                               |
| POST   | `/submissions/{submission_id}/reviews/`                     | Add a review/comment                              |
| POST   | `/submissions/{submission_id}/reviews/{review_id}/dismiss/` | Dismiss a review                                  |
| POST   | `/submissions/{submission_id}/merge/`                       | Merge (owner/maintainer only)                     |
| POST   | `/submissions/{submission_id}/close/`                       | Close without merging                             |

For direct product updates, `/submissions/validate/` returns an advisory
`product_update_preview`. Compare `current` and `projected` coverage, score
breakdowns and display tiers, then inspect `newly_known_fields`,
`refreshed_evidence_fields`, and `unchanged_fields`. Deltas are projected minus
current. A zero-delta re-attestation can still refresh useful evidence.
`unsupported` or `unavailable` status includes a reason and null snapshots. The
preview assumes accepted claims, does not approve citations, and cannot
guarantee the result against concurrent catalog changes. Validation runs no paid
checks and leaves no persistent catalog changes.

Submission mutations are throttled at **20 / minute** with a **5 / second**
burst.

## Feedback (auth required)

One-way intake for reports about the *service, API, or docs* (a bug, feature
request, or docs problem) — distinct from catalog submissions (data changes) and
product reviews (product opinions). Submit-only: no read, list, update, or
response path.

| Method | Path         | Purpose                                                  |
| ------ | ------------ | -------------------------------------------------------- |
| POST   | `/feedback/` | File feedback about the service (bug/feature/docs issue) |

Body: `title` (plain text, ≤ 200 chars), `body` (plain text), optional `context`
(`path`, `method`, `expected`, `actual`, `severity` = `low`|`medium`|`high`,
`reference_url`). There is no submitter-set category — classification is applied
at triage. `201` returns a receipt `{id, title, created_at, submitted_by}`; the
`body`/`context` are not echoed back. Over-length `title`/`body` are rejected
(`422`), never truncated. Throttled at **15 / hour** per account. The MCP
server, WebMCP, and the A2A adapter wrap this as a `submit_feedback` tool, and
the `oag` CLI as `oag feedback`, so an agent reports a problem from the tools it
already uses.

## Schema and docs

| Method | Path            | Purpose          |
| ------ | --------------- | ---------------- |
| GET    | `/openapi.json` | OpenAPI 3.0 spec |
| GET    | `/docs/`        | Swagger UI       |

Operation IDs in the spec are camelCase (e.g. `listProducts`,
`createSubmission`), so client generators produce idiomatic method names.

## Conventions

- **IDs**: UUID v4.
- **Timestamps**: ISO 8601 with timezone (`2026-06-04T12:00:00Z`).
- **Pagination**: cursor envelope
  `{ count, next, previous, page_size_default, page_size_max, results }`.
  `count` is the filtered total before pagination. Follow `next` until `null`;
  do not treat the cursor as a page index.
- **Errors**: `{ "code": "<ENUM>", "detail": "<human readable>" }`.
- **Rate limits**: see [Rate limits](#rate-limits) for response headers.
- **Submissions**: `payload` accepts scalar fields plus relation envelopes —
  reference/taxonomy many-to-many (`add` / `remove`, taxonomy also `propose`)
  and reverse foreign keys (`create` / `remove`), which nest. See
  [batch-populating.md](batch-populating.md) for the nested org+product shape.

## Rate limits

| Surface                 | Limit                          |
| ----------------------- | ------------------------------ |
| Anonymous catalog reads | 25 / minute / IP               |
| Authenticated reads     | 120 / minute / account         |
| Submission mutations    | 20 / minute + 5 / second burst |
| Signup                  | 10 / hour / IP                 |

Throttle responses return HTTP 429 with `code: "rate_limited"` and `Retry-After`
in integer seconds. `X-RateLimit-Scope` identifies exhausted budgets: `anon` for
anonymous IP reads, `global_auth` for account reads, and `submission` or
`submission_burst` for submission mutations. Multiple exhausted budgets appear
in sorted, comma-separated order. Account budgets span tokens. Pause all workers
that share the exhausted budget for at least `Retry-After` seconds. Add jitter
before resuming. The delay does not reserve a request slot.

Signup responses that reach the endpoint also include `X-RateLimit-Limit`,
`X-RateLimit-Remaining`, and `X-RateLimit-Reset`. Earlier shared-origin
rejections include `Retry-After` and `Cache-Control: no-store`. Successful
catalog reads do not promise rate-limit headers.

The cap of 25 open submissions per account produces a separate HTTP 429 without
`Retry-After` or `X-RateLimit-Scope`. Wait for existing submissions to merge or
close. Bulk submitters are exempt from this capacity cap.

The [CLI pacing reference](cli.md#pacing-and-workflow-deadlines) explains shared
reservations and cooldowns. Shell batch validation uses local pacing only;
coordinate other workers yourself or use `oag validate`.

## Error codes

Coded errors (`401`, `403`, `404`, `429`) use the `{ "code", "detail" }`
envelope:

| Code                     | When                                           |
| ------------------------ | ---------------------------------------------- |
| `AUTHENTICATION_FAILED`  | Missing, invalid, or revoked token             |
| `INVALID_PARAMETER`      | Query / body field has the wrong shape         |
| `MISSING_REQUIRED_FIELD` | Required input absent (signup, submissions, …) |
| `rate_limited`           | Throttle hit; honor `Retry-After` when present |

(Unknown codes from the live API should be treated as opaque — log the full
envelope and surface it to the caller verbatim.)

**Validation failures (`400`) do not use `code`/`detail`.** A payload field the
proposal validator rejects comes back as
`{ "errors": { "<field path>": ["message", …] } }`; read `.errors`, keyed by
field path. See "Errors" in SKILL.md for all three shapes (coded, validation,
conflict).
