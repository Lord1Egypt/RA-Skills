# Product fields and trust evidence

Read this when drafting product descriptions, trust claims, or scored fields.

## Draft for depth: fill every decision-axis field you can cite

The [source evidence rules](source-evidence.md) govern *what you may emit* —
only cited claims. It does **not** tell you to aim low. The two are easy to
conflate: because an uncited field sinks the whole submission, the safe-looking
move is to submit the minimal cited core (name, category, description, `url`,
maybe one capability) and skip everything else. That buys a clean merge and a
**shallow** record — and shallow records, not missing breadth, are the catalog's
binding constraint: mean field density across decision-relevant fields sits near
19%, and three of the four promised evaluation axes (cost, lock-in /
portability, trust) are near-empty catalog-wide.

So the drafting default is **fill, then justify omissions** — not *minimal
core*. For every product, work the full decision-axis field set below: fetch the
vendor's trust / security / pricing / docs pages and emit **every** field those
pages support. This is a target for the product's *record*, reached across as
many submissions as it takes — not a demand to cram everything into the initial
create. Land what you can cite now and add the rest in follow-up `update`
submissions (see the depth bar below). Drop a field only when it is **genuinely
uncitable** (no source states it), and when you drop one, say *why* in the
submission `description` (or your run notes) so the omission is a decision, not
an oversight. A field you *could* have cited but skipped for good to save effort
is exactly the failure this ends.

This neither relaxes the citation bar nor licenses guessing. The
asserted-negative booleans (`open_source=false`, `self_hostable=false`,
`no_proprietary_sdk`, `documented_provider_swap`, `account_required=false`) stay
**unset unless you actually checked** — either leave them unknown, or, when a
scoped look at the page that would carry the capability came up empty, record a
confirmed absence via `absence_attestations` (see
[confirmed absences](source-evidence.md)). Prefer the attestation: a confirmed
absence counts toward `coverage_score` (the Unrated/40% bar) exactly like a
positive, so a product with few citable positives — a hosted service that is not
open source, not self-hostable, exposes no A2A server — can still clear the bar
by attesting the absences you actually checked; leaving those fields merely
unset keeps it Unrated. What changes is the citable-but-habitually-skipped
fields.

**The decision-axis field set.** These are the signals that feed
`ai_native_score` (see `catalog/scoring.py`) plus cost — a product that leaves
them blank cannot be ranked or compared:

- **Cost:** `pricing_url` (the page you read prices off — almost always
  citable); structured `offers` only when the amount and billing period are in
  the fetched HTML (single-page-app pricing that renders client-side is the
  known-hard wall — omit, don't guess).
- **Trust:** `trust_center_url`; `compliance_certifications` from a static trust
  page; `no_training_on_user_data`, `zero_data_retention`, and
  `sandbox_environment`. These three fields use enums. A trust page stating "we
  do not train on your data" can support `no_training_on_user_data=yes` when the
  guarantee covers the product. A guarantee on an Enterprise-only page leaves
  other plans unknown; `available` needs an explicit restriction or contrasting
  plan policies. For a conditional no-training policy, both "we don't train
  unless you opt in" and "on by default, opt out in settings" support
  `available`. Reserve `yes` for an unconditional default guarantee within the
  vendor-managed service, including vendor-selected LLM providers. `available`
  asserts a condition; it is not a cautious substitute for `yes`. Check the
  cited policy for the condition before choosing it. In the Semgrep submission,
  the cited default zero-data-retention agreement supported
  `no_training_on_user_data=yes`; `available` failed because the evidence gave
  no condition. Assess each field against its own definition and the full
  policy; a zero-data-retention label alone does not establish a no-training
  guarantee. The field covers non-public data reuse for generative AI, including
  foundation models. Predictive ML for recommendations, search ranking or fraud
  detection and training on public data are outside scope. A guarantee can
  therefore support `yes` while allowing those uses. Cite the distinction in the
  submission. Generative models trained for recommendations remain in scope. A
  predictive ML opt-out alone does not establish `available`; unclear model type
  or a public-data exception alone establishes no guarantee. Customer-directed
  fine-tuning solely for a private customer model is also outside scope.
  Customer-configured external providers follow their own policies; that
  exception alone does not downgrade `yes` or establish consent to training.
  Evidence must cover the vendor and its selected providers. Cite the positive
  value whenever the page supports it. A verified `trust_center_url` earns +1
  raw Trust point, capped with the other Trust signals at 6 points and weighted
  at 30%. It must be a trust center or security-assurance portal that gives
  readers access to the vendor's compliance certifications and attestation
  reports — a downloadable or access-gated SOC 2 report, a certification listing
  that links that evidence, or an embedded SafeBase / Vanta / Drata / Oneleet
  portal. A general security overview, a page that only describes security
  practices, a privacy policy, or a terms-of-service page does not qualify, even
  when it names certifications in prose; `trust.<vendor>` subdomains and
  `/trust-center` paths usually qualify, a bare `/security` marketing page
  usually does not. Preflight the page with the verifier's fetch tier. The
  pointer-content check must load it and corroborate its kind and applicability
  to the product or publisher. Shared publisher portals can qualify; unrelated
  portals and a populated URL alone earn nothing. Re-submit a legacy URL to
  establish verification. Keep certification claims separately cited; privacy
  and ToS URLs earn no points. See the
  [scoring methodology](https://www.openagentguide.com/methodology/).
- **Portability / lock-in:** `data_export` / `data_import` (enums — see
  [portability evidence and repairs](portability.md) for coverage and fidelity,
  cited to a docs/import/export page); `open_standards`;
  `standard_protocol_access`; `self_hostable=true` and `open_source=true` (with
  `source_code_url` + `licenses`). The `true` direction of each boolean is
  citable; only the `false` direction is the uncitable negative above. The
  chosen `full` or `partial` level is itself a fact-checked world-claim: cite a
  page supporting that specific level, and use `partial` only when the page
  shows the import or export capability exists.
- **Security:** `multi_factor_authentication` (`available` / `enforced`, cited
  to a security page that names it) and `access_controls` (RBAC / GBAC / ABAC) —
  per "Cite each … RBAC / MFA association" below, which covers the
  static-vs-JS-rendered page trap. MFA needs the literal type; an access-control
  mechanism is corroborated behaviorally (cite the page documenting it — e.g.
  group-to-role mapping for `GBAC` — without needing the acronym).
- **AI-native affordances:** `mcp_servers` (cite the docs page), `api_specs`,
  `command_line_interfaces`, `developer_kits`, `agent_skills`, `web_mcp`,
  `headless_signup`, `native_connectors`, `a2a_servers` — use
  [integration evidence](integration-evidence.md) for their citation
  requirements.

Most of these (MFA, compliance certs, data-export, MCP / SDK / CLI support) are
stated plainly in vendor docs — filling them is drafting effort, not a
citability wall. Only structured **cost** is genuinely hard.

**Depth bar — accrued across submissions, not crammed into one.** A clean merge
of a thin record is **not** the goal; a deep *record* is. You do **not** have to
land every decision-axis field in the initial product create. Submissions are
immutable but **additive**, so depth accrues: land a solid cited core now, then
add trust / pricing / affordance fields in follow-up `update` submissions as you
work each vendor page. For each field, choose one of three dispositions: (a)
cite it in this submission, (b) defer it to a planned follow-up update, or (c)
omit it when the available sources cannot support it. Record the reason for each
deferred or omitted field. For a batch of products, report both accepted
submissions and the mean number of populated decision-axis fields per product.
This shows whether the batch improves the depth of the records it touches.

**Batch each submission's claims by their sources — don't shove everything into
one.** The reason to spread depth across submissions is not just ergonomics: the
fact-check is **all-or-nothing**, so one unsupported claim rejects the *entire*
submission. The more fields you pack in, the larger the surface for a single
weak citation to sink everything with it, and the more you re-draft on a reject.
A reliable strategy is to scope each submission to the claims supported by **one
to three information sources**: fetch a page (a trust center, a pricing page, a
docs page), add the fields that page cites, and submit; the next source becomes
the next `update`. Every claim in a submission is then backed by evidence you
read together, the blast radius of any one citation failing is small, and a
reject points at a tight, obvious set of fields instead of a sprawling one.

## Factual claims in catalog descriptions

Keep catalog descriptions descriptive and citable. Omit promotional superlatives
and comparative superiority claims such as "best", "leading", "most advanced",
"fastest", "number one", and "state-of-the-art", even when a cited vendor page
or benchmark repeats them. Attribution or quotation does not make these claims
acceptable catalog copy. Describe documented functions, supported interfaces,
and concrete limits instead. For example, replace "the best AI coding assistant"
with "A coding assistant with code completion and chat", with evidence for those
capabilities. This applies to descriptions at every payload level, including
offers and integrations. Judge the claim in context; ordinary technical terms
such as "best-effort delivery" are not superiority claims. Benchmark comparisons
and links to benchmark results are future work and do not create an exception to
this description policy today.

Payload `description` fields, including nested product descriptions, enter
fact-check claim extraction. Product descriptions are published to humans and
agents. Each material factual assertion needs cited semantic support, including
acquisitions, official SDK languages, typography capabilities, output formats,
and credit limits. Neutral summary wording needs no verbatim quotation.

Put supporting evidence URLs in the submission-level `description`, which
remains the change justification and evidence source, separate from the catalog
text in `payload.description`. Cite each factual assertion you retain. Remove
unsupported details; moving them from a structured field into prose does not
exempt them. Use structured fields where available without adding uncited claims
to the summary.

**Scope every claim — in descriptions and in attestation `method` text — to
exactly what the cited page states.** Fact-check decomposes a sentence into
separate world-claims and fails the submission on whichever half the page does
not support, so a conjunction or an unverified characterization sinks an
otherwise-cited claim. "Sends and receives SMS" is two claims — drop "and
receives" unless the page shows receiving. "Exposes a REST API" smuggles in
"REST" as a claim — write "exposes an HTTP API" unless the page names REST.
Prefer the narrowest wording the evidence supports over the fuller phrasing you
could not fully cite.

## Keep provenance out of `description` — no "verified on `<date>`" line

The submission-level `description` supplies evidence URLs and change context; it
is not extracted as catalog prose. Payload descriptions are claim-bearing. Keep
verification dates and first-person research notes out of catalog text.

Write the submission-level `description` as evidence URLs plus a neutral summary
of what changed.

## Policy direction: "attestation, not audit"

The governing principle for everything you submit: **every field needs a
supporting source, and that source can be the vendor's own marketing or docs.**
The bar is *attestation* — the claim is stated or supported on a citable page —
**not** *audit*: we confirm a trust page lists "PCI-DSS"; we never re-audit the
report. Good practice regardless of what is enforced today: give every field a
citable source, and prefer the vendor's own page.

Both changes in this policy direction have **shipped**:

- **Editorial taxonomy is corroborated (enforced now).** `categories`,
  `capabilities`, and `jobs_to_be_done` are claim-bearing: each is checked
  *semantically* against the vendor's own cited pages (no exact-string match, no
  per-term citation field). Only attach a capability / job / category the
  vendor's cited homepage or docs actually support — an uncorroborated tag is
  turned back with the field named, so don't mint aspirational taxonomy. The
  same semantic match means a compliance label resolves whether the page uses
  the acronym or the spelled-out name (a page naming the "Health Insurance
  Portability and Accountability Act" supports a `HIPAA` tag).
- **Pointer URLs are content-verified (enforced now).** A typed `*_url` is no
  longer reachability-only: the `pointer_content` check fetches each typed
  pointer's page and verifies it actually **is** that kind of page (a
  `trust_center_url` gives access to compliance certifications and attestation
  reports, a `pricing_url` shows plans or prices, an `api_specs[].url` parses as
  a spec, and so on). See
  [typed pointer evidence](integration-evidence.md#typed-pointer-urls-must-lead-to-the-right-kind-of-page).
  The fetcher renders JavaScript and escalates to an anti-bot tier (ZenRows)
  when a page blocks the primary fetch, so JS-heavy and lightly bot-gated pages
  are read fine; a page that blocks even that tier is a negative signal about
  the product and hard-fails. Prefer pointer pages whose content plainly matches
  their kind.

## Cite each compliance cert — and each RBAC / MFA association — to the plainest static page that names it

A compliance-cert claim survives only if the crawler renders the cited page's
text and that text literally names the cert. A SafeBase-style trust center (e.g.
`security.vendor.com`) that lists "SOC 2 Type 2", "ISO 27001", "PCI-DSS" as
plain HTML fact-checks cleanly; a JS-heavy trust center whose cert list is in
the rendered DOM but not the fetched HTML does not — SafeBase SPAs such as
`trust.datadoghq.com` render the whole cert list client-side, so the fetched
HTML contains none of the cert strings a browser plainly shows.

**Pre-flight every cert against the fetched HTML before attaching it.** Fetch
the raw HTML the way the crawler sees it — no JavaScript execution — and grep
for each cert string; attach only the certs that match:

```bash
curl -sL "https://trust.vendor.example" | grep -i -e "soc 2" -e "iso 27001" -e "hipaa"
```

No match means the string is absent from the fetched HTML, so the cert comes
back `insufficient_evidence` however plainly the browser renders it — do not
attach it on the strength of the rendered page.

Check each certification independently; the grep is per-cert. A partly static
page may substantiate SOC 2 and ISO 27001 while HIPAA appears only after
JavaScript runs — expect to drop individual certs even off a page that
"obviously" lists them. If a cert returns `insufficient_evidence`, find a
fetchable source for that cert or drop that association when resubmitting; keep
the certs that have support. If *no* cert on the page survives the pre-flight,
drop the compliance associations and submit the product on its category /
capability classification alone — a product with no certs still merges, where a
single unverifiable cert fails the whole submission. Taxonomy tags also require
evidence. Cite the vendor page that supports them under the
[taxonomy evidence rules](taxonomy-evidence.md).

Keep descriptions within what the cited product or security pages substantiate.
Do not add capability claims such as private or on-premises deployment from
assumptions about the vendor.

`mfa_types` follows the **same exact-string rule**: it is a world-claim held to
the citation bar exactly like a cert, and page-render-dependent in the same way
(supported off a plainly-listed security page, `unsupported` off a JS-heavy
one). Cite each MFA type to the plainest static page that literally names it
("passkeys", "TOTP"), not a marketing overview whose text renders client-side.

`access_controls` is a world-claim too, but it is corroborated **behaviorally**,
not by the literal label: cite the plainest static page that documents the
mechanism's defining behavior, and the acronym need not appear. A page
documenting that identity-provider or directory groups map to roles or
permissions supports `GBAC` ("group-based access control") even when it never
writes "GBAC"; named roles granting permission sets support `RBAC`. Keep the
mechanisms distinct — SSO or SCIM provisioning alone, generic user provisioning,
and individually assigned roles do **not** support `GBAC`, because none maps a
group to a role — and keep any plan or edition restriction (e.g. SSO/SCIM group
mapping gated to Enterprise) in the evidence. The page still must render the
describing text in the fetched HTML, so the same JS-heavy-page caveat applies.

## Declare a dimension not-applicable only when it genuinely doesn't fit

`dimension_applicability` is a per-dimension list (not an add/remove envelope)
that marks a scoring dimension (`integration`, `trust`, `portability`,
`security`) as not-applicable to the product's category, excluding it from the
AI-native score. Each entry needs a `justification` grounded in the product's
nature (no source citation — it is an editorial judgment), e.g. an open-source,
self-hosted library that operates no hosted service has no `trust` surface. A
guardrail rejects any declaration that would leave fewer than two applicable
dimensions or less than half the nominal scoring weight, so use it sparingly —
most products leave every dimension applicable.
