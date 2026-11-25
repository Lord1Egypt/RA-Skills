# Publisher and product identity

Read this before creating products, resolving publishers, or changing product
identity.

## Separate products from plans

Use one Product for each offering the publisher publicly markets as a separate
product. Cite the vendor's product pages or product directory to establish the
boundary. A shared domain, account, SDK, or billing system does not make sibling
products one Product. For example, PostHog Product Analytics, PostHog Session
Replay, PostHog Feature Flags, PostHog Experiments, and PostHog Surveys belong
in separate entries under the PostHog Organization.

Keep Free, Pro, and Enterprise plans as Offers on their Product. Monthly/annual
purchase choices belong in that Offer's prices. A feature, integration, or
pricing meter alone does not establish a separate product. Attach each Offer to
the product its pricing covers. Copy shared affordances or policies only when
the evidence establishes that they apply to the specific product.

Before creating an entry, inspect existing products under the publisher. Update
a matching product instead of creating a duplicate. When repairing a combined
entry, inspect its offers, claims, relations, and public reviews. Consider the
effect on existing bookmarks when choosing which product retains its identity.
Preserve the existing UUID and slug when they can accurately represent that
product, narrow its name, description, and pointers, and create the other
supported products separately. Reassess retained claims and relations against
the narrowed scope; move or remove mismatched content through the supported
workflow. The reviewer may not receive unchanged fields, so the submitter must
audit the complete retained record. Do not copy the combined entry's score or
claims to its siblings. Record the mapping and evidence in the submission
justification and verify the resulting product and offer records after merge.

## Resolve publisher identity before creating records

Before drafting a Product or publisher create, record the publisher's name,
`Person` or `Organization`, primary-source URL and passage, and why that
evidence identifies that kind of publisher. Search both People and
Organizations, plus Products, using current and former names and official
domains. Inspect likely matches and record the identity to reuse, or why a new
publisher is needed.

Use `Person` when primary evidence identifies an individual as the
maker/operator. For example, evidence identifying Dmytro Krasun as
ScreenshotOne's individual operator calls for a Person-based draft. Use
`Organization` when evidence identifies a company as the publisher. For example,
an official page stating that fictional Cedar Labs Ltd operates Birch calls for
an Organization-based draft, even if the page also names its founder. A
commercial product, brand, solo founder, or company-like username alone does not
settle the publisher kind. If legal/operator identity is unclear, record the
unresolved research question and obtain evidence before creating either record.
Do not silently switch kinds to make a draft fit.

Read the matching live writable schema at
`/api/v1/submissions/fields/?app_label=catalog&model=person&include_nested=true`
or the same endpoint with `model=organization`. For a nested product, use the
chosen publisher model and its schema's `products.create` relationship; the
product inherits that publisher. Reuse a matching publisher through an update or
a direct Product create referencing its identity, according to the live schema.
Read the Product schema for a direct create and set exactly one of `person` or
`organization`. Before validation and the first write, compare the recorded
decision with the submission model and publisher relationship. Keep the decision
in research notes and submission-level justification, with publisher citations
retained in the payload; it is not an extra API field.

For an acquisition, establish who currently publishes the product and search
both former and current publisher names. If Cedar acquired Birch from Birch Labs
and now publishes it, reuse Cedar's matching identity. A rename of the same
company reuses its identity; an acquisition alone does not establish that two
Organizations are the same entity.

## Scope capabilities and licenses to editions and components

Read official edition comparisons, component documentation, and applicable
license files before asserting a capability or license. Establish which edition,
component, deployment, or plan each passage covers. An open-source connector's
license does not establish the license of its hosted platform. Keep plan-only
capabilities in the appropriate Offer description with their restrictions; do
not turn them into an unqualified Product claim.

For example, if fictional LakeDB documents Parquet export only for Enterprise, a
proposal for LakeDB Open Source must omit that capability unless a primary
source also establishes it for Open Source. An Enterprise Offer may describe
Parquet export with the edition-specific citation. Follow the product-boundary
rules above when deciding whether editions are separate Products or Offers; an
edition label alone does not settle that decision. Apply the same scope check to
prices using [pricing-evidence.md](pricing-evidence.md).

## Attribute marketplace products to their publisher

For a marketplace app, plugin, Actor, or community integration, identify the
publisher from the listing's developer/byline and linked publisher profile. The
host platform is not the publisher merely because it hosts, distributes, bills
for, or supplies APIs to the product. A first-party product can use the platform
organization when the evidence identifies it as the developer. Use `person` for
an identified individual and `organization` for an identified company or
project. Do not infer a company from a username containing `llc`. For example,
the Apify listing for Product Directory Submitter identifies Mark Rieck
(`prodmarkllc`) as its community developer, so its publisher is that person, not
Apify. A publisher profile hosted on the marketplace is valid identity evidence;
an independent domain is not required.

After establishing the publisher's kind and identity, its first-party product
homepage can support the publisher relationship when it presents the product
under that publisher's name. A separate "published by" page or marketplace
byline is unnecessary in that case. This relationship evidence does not by
itself establish that the publisher is an Organization. Apply the publisher
selection step above before choosing the parent model.

Check this relationship for direct product submissions and nested
`products.create` entries, which inherit their parent publisher. Record IDs and
slugs need no verbatim citation, but the publisher relationship needs supporting
evidence. A passed check does not establish that relationship. If attribution is
missing or contradicted, name the product, the proposed `organization`/`person`
or nested payload path, and the missing or conflicting developer evidence.
Request the correct publisher and a supporting listing or profile; do not
substitute the host when the developer is unknown.

## Change an existing product's publisher

Read the product by UUID and resolve the intended publisher before submitting.
People support `?name=<exact-name>` and `?slug=<slug>`, not `search`. Reuse an
existing publisher; if absent, submit its creation and wait for merge before
referencing its UUID. Read `/submissions/fields/` for the live shape.

Submit an `update` against the existing product UUID. Payload relation names are
`organization` and `person`, although catalog reads return `organization_id` and
`person_id`. To move from an organization to a person:

```json
{"organization": null, "person": "<person-uuid>"}
```

Set both fields in the same submission when switching types; exactly one must be
non-null. For the reverse move, set `person` to null and `organization` to the
new UUID. To change publishers of the same type, replace that relation. Cite the
product listing and publisher profile in the submission description. Do not
recreate the product or resend its unrelated fields and child records. Validate,
submit, wait for checks and review, then have a curator merge. Read back by
product UUID and verify both publisher fields and the rendered product page.
Publisher changes can change the public product URL; check the old URL too and
record any broken links rather than assuming a redirect.

## Organization websites identify the organization

For an organization, set `url` to the official company, lab, or project's
homepage. Prefer that site; an official organization-level GitHub page is an
acceptable fallback. Do not copy a product page, individual repository, package,
or documentation page into the organization website field. For example, .NET can
use `https://dotnet.microsoft.com/en-us/` or `https://github.com/dotnet`, not a
particular .NET library's repository. A project homepage can contain a path or
share a domain with its parent company; choose by what the page represents, not
by URL shape. An organization and product may share a homepage when it
represents both.

For a correction, submit an organization `update` containing only `url`, with
the reason and official source in the submission justification. Homepage URLs
remain exempt from separate fact-check citations and typed-pointer content
checks; reviewers and curators still reject demonstrated subject mismatches.

## `url` is the canonical homepage; the docs portal goes in `documentation_url`

Use the product's official homepage for `url`, including for open-source
projects. Put its implementation repository in `source_code_url`. Use the
repository for `url` only when the project has no separate official homepage; in
that case, both fields can contain the same repository URL.

For example, SpiderFoot has separate homepage and implementation URLs:

```json
{
  "url": "http://www.spiderfoot.net/",
  "source_code_url": "https://github.com/smicallef/spiderfoot"
}
```

Check redirects and confirm the page still represents the product. In the
October 20, 2026 SpiderFoot correction, its homepage redirected to Intel 471.
Keep the product homepage, publisher identity, and implementation repository
separate. A redirect alone does not establish the publisher relationship; check
applicable official product or publisher evidence before assigning it.

Put the docs home in `documentation_url` and pricing in `pricing_url`. Link
specific docs resources, such as API references and SDK guides, through
`documentation_resources`. The `urls` check covers homepage reachability;
`documentation_url` also receives the
[typed-pointer content check](integration-evidence.md#typed-pointer-urls-must-lead-to-the-right-kind-of-page).

## Product source means the product's implementation

Set `source_code_url` only for the cataloged product's own implementation. An
official SDK, API client, CLI, example, integration, or docs repository for a
hosted service is not that service's source. For example,
`https://github.com/apify/apify-sdk-js` belongs in Apify's `developer_kits`, not
the Apify platform's `source_code_url`. Use the matching integration or
`documentation_resources` relation for other supporting artifacts. If the
cataloged product is itself an SDK, CLI, or library, its implementation
repository does qualify.

Point `source_code_url` at the specific repository (`github.com/<org>/<repo>`),
not the GitHub org or user profile page (`github.com/<org>`). The
pointer-content check fetches the URL, and a bare profile landing page lists
repositories rather than being the product's source, so it hard-fails as the
wrong kind of page. Vellum's `github.com/vellum-ai` was rejected for this
reason.

Read what the repository implements before submitting it. A supporting tool's
license or local installation instructions do not establish the hosted product's
`open_source`, `licenses`, or `self_hostable` values. Cite evidence for the
product itself. If its source is unknown or unpublished, omit `source_code_url`;
do not substitute a client repo or infer negative booleans. To correct a stored
SDK link, submit an update clearing `source_code_url` with `""` and record the
SDK under `developer_kits` without duplicating an existing kit.

## Match evidence to the product's coverage scope

Establish both what a source says and which product it covers. Company-wide
compliance evidence can support a product when the stated scope covers all of
that company's products and the product belongs to that company. It need not
name every product separately. When coverage is limited to selected products,
services, plans, or deployments, require evidence that the product is included
and retain those restrictions. SOC 2 might cover all company products while PCI
DSS covers only a payment service. Read the scope for each claim; do not infer
it from the standard's name.

Hosting does not transfer the host's claims to third-party products. An Apify
Actor does not inherit Apify's SOC 2, GDPR compliance, CLI, MCP server, or
OpenAPI spec merely because it runs on Apify. Shared tools can qualify when
evidence establishes that they actually serve the cataloged product. A shared
domain, marketplace listing, reachable endpoint, or valid OpenAPI document alone
does not establish that relationship. Keep identity-field citation exemptions,
but do not attach a demonstrably unrelated affordance.

Record the product, cited source, and coverage scope with each claim. For an
unsupported or uncertain compliance scope, obtain a coverage citation or omit
the association. A `supported` fact-check verdict or approved review does not
override a scope mismatch. Curators should name the affected payload path,
claimed subject, actual source scope, and missing evidence when rejecting.

## Cite a product's own page, not a parent's portfolio homepage

When a company pivots or renames, its root homepage can shrink to a portfolio
page that routes visitors to several products instead of describing any one of
them. Point the product's `url` at the page that represents *that* product. When
you cite evidence for a fact-checked claim, cite that product-specific page too
— or its docs or source repo — because the portfolio root carries little
product-specific text. A claim cited to the root comes back
`insufficient_evidence`: the page genuinely does not state it, and the repair is
to cite the richer product-specific page.

Hasura shows the shape. `hasura.io` now renders about 700 visible characters
routing to two products — Hasura DDN at `hasura.io/ddn` and the separately
branded PromptQL at `promptql.io`. Claims about Hasura DDN's features,
capabilities, and affordances belong to `hasura.io/ddn`, its documentation, or
its GitHub repository; the `hasura.io` landing page names the products but
documents neither.
