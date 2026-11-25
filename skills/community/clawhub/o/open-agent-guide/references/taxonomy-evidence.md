# Categories, capabilities, and documented tasks

Read this when changing categories, capabilities, jobs to be done, or documented
tasks.

## Review categories, capabilities, and jobs to be done together

During initial product research and enrichment, assess all three relations,
including when the assignment focuses on a category:

- `categories` describe the kind of product, for example **Deep Research**.
- `capabilities` describe what it can do, for example **Multi-step research**.
- `jobs_to_be_done` describe the user's goal, for example **Research a topic in
  depth**.

These are distinct associations. Category membership alone does not establish
that the product supports a capability or serves a job. Do not copy the same
wording into all three relations or require a new term for every product.

1. Read the current product's associations and the published vocabulary at
   `/api/v1/catalog/categories/`, `/api/v1/catalog/capabilities/`, and
   `/api/v1/catalog/jobs-to-be-done/`. Follow pagination and check equivalent
   meanings as well as names before proposing terms.
2. Compare each relation with the product's primary sources. Reuse equivalent
   published terms by slug. Propose a new term only when no equivalent exists
   and the sources support its meaning and the product's association with it.
   Keep the existing citation and verification requirements for each relation;
   assess capabilities and jobs semantically from the cited pages.
3. Preserve existing associations unless evidence supports a correction. Submit
   only changes through `add`, `remove`, or `propose`; omit unchanged relations.
   A category-focused assignment still needs the capability and job assessment,
   even when neither needs a change.
4. In the research and final reports, cover each relation: supported
   associations already present, changes proposed, and anything deliberately
   left unchanged or unresolved, with reasons and evidence or evidence gaps.
   Distinguish proposed changes from confirmed published associations after
   submission.

For example, sources describing a product that conducts iterative research to
produce an in-depth answer may support the Deep Research category, Multi-step
research capability, and Research a topic in depth job. Check the published
vocabulary and the specific product's evidence before attaching any of them. If
one association is already present, retain it and report it; if support for
another is uncertain, leave it unresolved rather than inventing a term.

For supported additions, the payload can reuse existing terms and propose a
missing concept inline:

```jsonc
"capabilities": {
  "add": ["brand-asset-retrieval"],
  "propose": [ { "name": "Web Navigation", "slug": "web-navigation", "description": "…" } ]
},
"jobs_to_be_done": {
  "add": ["find-brand-assets"],
  "propose": [ { "name": "Automate a browser workflow", "slug": "automate-browser-workflow", "description": "…" } ]
}
```

A proposed slug that **exactly** matches an existing one just links the existing
row (deduped), so re-proposing a known term is safe. A *near*-duplicate with a
different slug (e.g. proposing `data-scraping` when `web-scraping` already
exists) is **not** auto-merged: the advisory `taxonomy_dedup` check compares
every newly proposed term against the existing vocabulary and records
near-duplicate candidates for the curator. It never rejects a submission, but it
does mean the curator may ask you to reuse the existing term — so search the
vocabulary first (`GET /capabilities/`, `/jobs-to-be-done/`, `/categories/`) and
prefer an existing term over minting a slight variant. A `capability` names
*what the product can do* ("Web Navigation"); a `jobs_to_be_done` names *the
user goal it serves* ("Automate a browser workflow") — phrase each accordingly,
not as a marketing feature.

## Documented task completion

Use `documented_task_completions` in a product payload to describe whether an
agent can finish a specific job through one selected route, based on cited
provider documentation. Resolve `job_to_be_done` as an existing slug or UUID
from `/api/v1/catalog/jobs-to-be-done/` and include that job in the product's
`jobs_to_be_done`. Keep one record per product/job. All assessments must
describe the same route. Set `route_kind` to `api`, `mcp`, `a2a`, `cli`, `sdk`,
`webmcp`, `agent_skill`, `native_connector`, `web`, or `prose`. Route references
`content_type`/`object_id` and per-step requirements are not writable.

Complete means delivering the linked job's main outcome **by and large**, using
its name and definition. The workflow may have prerequisites and limits on
eligible cases or scale, and may omit edge cases or optional features. Its scope
must preserve the job's essential outcome. A preliminary step alone qualifies as
`documented_partial` when evidence establishes that limited workflow; use
unknown when the evidence is inconclusive. A narrower job association is valid
only when that job actually matches the documented outcome and the product lists
it under `jobs_to_be_done`.

For "Manage project work" (plan tasks, assign work and track project progress),
investigating one bug and posting findings is partial. Planning, assigning and
tracking a small project can be complete, even with one-time account setup. The
job concerns managing work; it does not require implementing every task's
deliverable. A partial example does not establish that the product lacks other
complete workflows. Explain the supported outcome and any missing essential part
in `scope` and `conditions`.

`scope` must name the principal, exact outcome, prerequisites, setup/execution
boundary, and limits. `completion_support` accepts `documented_complete` or
`documented_partial`; each human requirement accepts `none`, `required`, or
`conditional`; `on_behalf_of` accepts `supported`, `conditional`, or
`prohibited`. For unknown assessments, omit the field or write `""`; reads
return `null`. Do not write `"unknown"` or infer `none` from silence. Partial
and conditional assessments require a cited handoff reason or trigger in
`conditions`.

A material prerequisite or limit that bears on selecting or executing the route
belongs in the public `scope` or `conditions`, which every read surface shows: a
beta or deprecated lifecycle with a named successor, a coverage or scale cap, or
a result-retention window. The submission `description` cites the source that
proves each qualifier; a limit left only in that submission evidence never
reaches the consumer. Keep this to the conditions that change how a consumer
chooses or runs the route, so a positive record stays concise instead of
absorbing every vendor fact. The Firecrawl Extract completion keeps its beta
status and documented `/agent` successor, its unsupported large-site and
exhaustive-enumeration cases, and its 24-hour result-retention window in
`conditions`, while the submission `description` names the documentation page
that establishes each.

These are hypothetical product payload fragments. Replace the job slug and
claims with fetched evidence, bind the product's `object_id` in an update
submission, and cite source URLs in the submission `description`. Validate at
`/api/v1/submissions/validate/` before submitting. The parent supplies
`product`. A complete API route after one-time human setup:

```json
{
  "jobs_to_be_done": {"add": ["resolve-support-tickets"]},
  "documented_task_completions": {"create": [{
    "job_to_be_done": "resolve-support-tickets",
    "route_kind": "api",
    "completion_support": "documented_complete",
    "setup_human_requirement": "required",
    "execution_human_requirement": "none",
    "on_behalf_of": "supported",
    "scope": "An authorized support agent resolves an assigned ticket through the API after an administrator grants access. Completion ends at ticket closure.",
    "conditions": "Administrator authorization is a one-time setup step."
  }]}
}
```

A separate partial route with conditional human involvement:

```json
{
  "jobs_to_be_done": {"add": ["resolve-support-tickets"]},
  "documented_task_completions": {"create": [{
    "job_to_be_done": "resolve-support-tickets",
    "route_kind": "web",
    "completion_support": "documented_partial",
    "execution_human_requirement": "conditional",
    "scope": "A support agent drafts a resolution in the web UI for an assigned ticket after account setup; final closure remains outside the documented agent route.",
    "conditions": "A human must approve resolutions involving refunds; the documentation does not establish agent-driven ticket closure."
  }]}
}
```

To replace a published record, send `remove: ["<completion-uuid>"]` and
`create: [{...replacement...}]` together inside `documented_task_completions`.
Get the completion UUID from the product detail API. There is no nested update;
removal runs before creation, so replacement preserves one record per job.

Credentials alone do not establish human-only setup. Confirmation
recommendations also do not establish a mandatory provider or technical
requirement. If Calendly confirmation advice fails to support
`execution_human_requirement=required`, omit that assessment and preserve the
advice in `conditions`; changing it to `none` requires separate evidence.
Recipient consent does not establish delegated permission. Keep unsupported
setup and delegation assessments unknown. Required repairs should identify the
smallest correction within these writable fields. Richer endpoint or capability
modeling suggestions are optional future modeling, not prerequisites for
acceptance.
