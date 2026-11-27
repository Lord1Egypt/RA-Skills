# Contribute to the catalog

[Submit your Product](https://www.openagentguide.com/submit-your-product.md)
explains both contribution paths. To request research without an account, use
the public form with a product name, homepage URL, description, and private
notification email, or email <support@openagentguide.com>. A product research
request is separate from a catalog submission and does not guarantee inclusion.
For direct catalog submissions, follow the authenticated workflow below.

Use this workflow only when the user's task authorizes catalog changes. Read the
references for the fields you are changing; unrelated field guides are optional.
Catalog reads and product decisions require no contribution.

## Prepare a proposal

1. Read the product and its coverage before changing an existing record.
   Preserve supported values and identify the gaps relevant to the task.
2. Establish product and publisher identity before creating records. Use
   [publisher identity](publisher-identity.md) for editions, plans,
   marketplaces, and canonical websites.
3. Fetch and read the sources for each claim. Follow
   [source evidence](source-evidence.md) for visible text, source previews,
   rendering-provider privacy, and confirmed absences. Leave unknowns unset.
4. Inspect the current writable schema. Group dependent claims together and
   separate independent claims with [proposal scope](proposal-scope.md).
5. Apply the relevant field guidance from the table below. Keep citations and
   qualifiers with their claims. Do not infer missing prices or capabilities.

| Fields being changed                                        | Read                                            |
| ----------------------------------------------------------- | ----------------------------------------------- |
| Product descriptions, trust claims, scoring applicability   | [Product field evidence](field-evidence.md)     |
| API specs, MCP, SDKs, CLIs, agent skills, documentation     | [Integration evidence](integration-evidence.md) |
| Categories, capabilities, jobs to be done, documented tasks | [Taxonomy evidence](taxonomy-evidence.md)       |
| Offers, billing terms, and prices                           | [Pricing evidence](pricing-evidence.md)         |
| Data import and export                                      | [Portability evidence](portability.md)          |
| Nested organization and product batches                     | [Batch contributions](batch-populating.md)      |

## Validate, submit, and watch

Put evidence URLs in the submission envelope's `source_urls` list. Keep each
claim and its qualifications in `description`. With this list, URLs mentioned in
prose stay as context; only the listed sources and structured URL fields become
verification targets. Use `[]` when there are no prose citations. Omitting the
list or using `null` retains URL discovery from prose.

Use the [CLI command reference](cli.md#submission-commands). Validate the
proposal before submission. Validation checks payloads and does not inspect
external citation URLs. Check those pages and their redirects separately.

Submit with a durable journal. Extract confirmed IDs from the result, then watch
them with a watch journal. Retain both journals. Resume an uncertain write with
the same submit journal; do not replay it with a fresh key.

Read [submission recovery](submission-recovery.md) when watching results or
repairing a rejection. Inspect terminal feedback before creating a corrected
proposal. Corrections use a new payload and journal. Superseding an open create
requires an explicit decision. A merged submission completes the contribution
workflow; check published values when the user's task includes that audit.

## Research an existing product's gaps

Use `oag coverage PRODUCT --output json` for one compact report of the product's
coverage and unknown scored fields. The default text output includes evidence
guidance. The equivalent reads are
`GET /api/v1/catalog/products/{uuid-or-slug}/coverage/` and the MCP tool
`get_product_coverage`. Read each gap's shared semantics, schema reference, and
absence page class before drafting. Keep unsupported values unknown. A confirmed
absence can improve coverage without improving the AI-native score. Use
submission validation to inspect projected changes after collecting evidence.

For product `budget_caps`, use `yes` only when a hard cap stops billable usage
by default, or `available` when it requires opt-in or has limited plan/service
scope. Cite official pricing, billing, or spending-limit documentation. Vendor
billing controls described as "max spend", "maximum spending threshold",
"spending limit", or equivalent wording support `available`. A pricing-page
feature label such as "Set maximum spend threshold" is sufficient. A separate
statement that usage stops is unnecessary. Usage alerts, spending alerts, and
threshold notifications alone do not qualify. Preserve explicit alert-only or
continued-billing qualifications. An optional setting alone does not support
`yes`.

Use `no_billing` for an entirely free product with no billable usage. Cite an
official pricing or free-usage page establishing that the whole product is free;
a free account or free tier within a paid product does not qualify. Billing
controls are unnecessary for `no_billing`. Use `no` for corroborated absence.
Preserve scope and overage qualifications in citations. Alerts, soft budgets,
rate limits and fixed subscription prices alone do not establish a cap. A `no`
value requires a whole-field `absence_attestations` entry with
`field_key: "budget_caps"`, `method`, `source_url`, and `checked_at`; the server
records the actor. Cite complete authoritative billing documentation for page
silence, or a scoped explicit negative quotation. Leave unknown values unset;
send an empty string to clear a prior value.

For example, after checking complete official billing documentation, submit this
product payload with the actual evidence URL, inspection time and method:

```json
{
  "budget_caps": "no",
  "absence_attestations": [
    {
      "field_key": "budget_caps",
      "method": "Read the complete spending-controls documentation; it describes alerts only and no hard spending cap.",
      "source_url": "https://vendor.example/docs/billing/spending-controls",
      "checked_at": "2026-10-21T12:00:00Z"
    }
  ]
}
```
