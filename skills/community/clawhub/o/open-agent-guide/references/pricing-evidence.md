# Pricing evidence and offer replacement

Read this when collecting prices or preparing offer replacements. The live field
schema determines which fields can be submitted. After deployment,
`pricing_options` holds multiple choices within one plan.

## Research the purchase terms

The checker reads each URL as loaded and does not navigate: it does not select
tabs, open accordions, dismiss dialogs, submit forms, or follow in-page links.
Cite evidence visible on initial load. If a control hides the claim, use a
direct link that opens with the claim visible, a docs page, or another source
that states it without interaction. Preview the exact URL with
`POST /api/v1/submissions/source-preview/` before submitting.

For example, annual terms behind a Yearly billing tab need a source that shows
them on initial load. A monthly default view cannot support those annual terms.

For each named plan, inspect official pricing and billing sources for both
monthly and annual options. Record the source URL and retrieval date in the
research journal, not as vendor claims in catalog descriptions. Keep each amount
attached to its product, plan, billing option and unit quantity. A shared
pricing URL or equal amount does not make two options interchangeable.

Distinguish the price denominator, invoice cadence and minimum commitment. A
rate per month alone establishes neither monthly payment nor cancellation
rights. Monthly invoices under a 12-month contract are not month-to-month.
Capture per-user, per-seat and per-1,000-request quantities explicitly in the
working evidence. Leave unstated terms unknown; do not infer them from the
billing-model tag or the default state of a pricing toggle. Yearly payment
cadence alone does not establish a minimum contractual term.

Preserve exact published charges. A $400/year charge has an approximate monthly
equivalent of $33.33; a rounded $33/month annual headline does not establish a
$396 annual charge. If the fetched source does not establish the real charge and
terms, retain the pricing URL and report the evidence gap. Do not fill it from a
competitor directory, tutorial example or another plan's price.

## Preserve edition and plan scope

Match each price and included capability to the named product, edition,
component, and plan in the primary source. A connector's license or a community
edition's free availability does not establish the hosted platform's license or
price. Preserve any license restrictions in the scoped description and cite the
applicable license or terms. Omit unrelated product claims from an Offer repair;
explicitly cite every affirmative claim retained in the submitted descriptions.

Read the entire relevant plan entry before asserting that no price is public.
"Contact sales" can appear alongside a published starting price or minimum. For
example, if an Enterprise plan says "from $500/month, contact sales," retain the
published minimum and its qualification in `price_description`; do not say that
pricing is unpublished or present $500 as an exact charge. Add a numeric option
only when the source supports its amount and terms under the schema below. A
failed fetch or missing amount in an excerpt leaves pricing unknown.

## Describe what the plan includes

For new offers and pricing or description updates, summarize the included
capabilities, published usage allowances and material eligibility or feature
restrictions from the cited sources. Use the Offer `description` for plan
coverage, `price_description` for shared conditions, and an option's
`description` for conditions specific to that option. Keep quantities and reset
periods explicit. A plan named Free with a free price still needs its sourced
coverage.

Put a condition that applies to every option in `price_description` once. Do not
repeat the same shared sentence on each option's `description`: the plan card
renders every option's `description` in a row, so a preamble copied across them
(for example "Additional to the base subscription …" on each usage tier) becomes
a wall of duplicated text. Each option's `description` carries only what is
specific to that option — its own usage tier, speed, or eligibility — and the
shared clause lives in `price_description`, which renders once for the plan.

Review rejects material omissions when fetched evidence supplies those details.
It does not require every feature-table row, other plans, or unpublished limits.
Keep unknown details unknown. Option labels distinguish billing choices, so when
a plan has several options that would otherwise show the same amount and unit
(per-speed or per-volume tiers, for example), put the distinguishing dimension
in each option's `label`. The ledger renders the `label` as the row heading, and
an option whose only distinguisher sits in `description` shows up as a repeated
price row. Omit a `label` only when the amount and unit already identify the
option and a label would merely repeat the plan name or formatted price.

## When research and verification show different prices

Treat a suggested replacement in check feedback as a value to investigate. If
your fetched price differs, compare the same product, plan, currency, billing
option, unit quantity, location and tax treatment before changing the amount. A
page can replace its initial price with a localized or tax-inclusive total after
JavaScript runs. Agreement between two fetches does not resolve a contradictory
third capture.

Read the failed check's `details.resource_snapshots` and the claim's
`supporting_passages`. Use `POST /api/v1/submissions/source-preview/` with the
exact cited `url`, the same `claims` and source mode, and the check's
`source_sha256` as `expected_source_sha256`. Save these diagnostics alongside
your research:

- Requested URL, including query parameters; reported URL; and any observed
  redirects. A provider-reported URL is not proof of the final vendor URL.
- Retrieval time, requested provider, configured anti-bot provider, degradation
  and recovery metadata. The configured fallback does not prove it was used.
- Full-source and selected-text hashes, selected pricing passages, completeness
  and selection mode. Hash inequality establishes changed text, not its cause.
- Cache configuration if available. Preview and verification share a five-minute
  cache keyed by URL, providers and timeout. Repeating a preview within that
  window can return the same capture. Provider caches are separate; a new
  preview does not guarantee a fresh origin fetch. Record unavailable cache or
  redirect details as unknown. Avoid query changes to force a matching price.

Seek an official source that establishes the conflicting price's scope. If you
cannot reconcile the captures, omit the disputed numeric option from the new
proposal, retain the pricing URL, and report both captures as an unresolved gap.
Preserve existing catalog options when constructing a replacement array;
omission must not silently clear them. Submit other supported claims separately
where possible. Do not copy the verifier's amount, average the prices, retry an
identical payload, or weaken the evidence requirement to obtain acceptance.
Preview is advisory and never authorizes a claim.

## Submit using the current schema

Keep one Offer per published plan. Put its monthly, annual and usage options in
`pricing_options`, a complete array replaced on update. Omission preserves the
current array; `[]` clears it. Each option has a unique stable `key` within the
plan and an optional `label`. The key is a required internal identifier: choose
any schema-valid value and retain it when repairing evidence failures. It needs
no vendor citation and its wording does not establish pricing terms. Supply
evidence for these terms:

- `price_kind`: `fixed`, `usage`, `free`, `custom` or `unknown`. Fixed and usage
  prices require a positive `amount` and `currency`. For explicit vendor free
  availability, use `{"key": "free", "price_kind": "free"}` with no
  denomination. The server returns amount `"0"` and blank currency, including
  for older currency-bearing free options. Keep sourced eligibility and usage
  restrictions in `description`; free alone does not establish no minimum
  commitment. Custom/unknown have no amount.
- `amount`: exact decimal string, up to 24 digits and 12 decimal places.
- `price_basis`: `charge` or `monthly_equivalent`. The latter requires
  `period: "month"` and retains a published monthly equivalent without inventing
  a charge.
- `period`: `hour`, `day`, `week`, `month`, `year`, `one_time`, or null if
  unknown or inapplicable. This is the price denominator, not payment cadence.
- `unit` and positive decimal-string `unit_quantity`: supply both for per-user
  or usage prices, such as `"requests"` and `"1000"`. Units are free-form text.
  Prefer lowercase words separated by spaces, such as `"audio minutes"`; avoid
  snake_case such as `"audio_minutes"`. Preserve the source unit's meaning.
- `payment_cadence`: `hourly`, `daily`, `weekly`, `monthly`, `quarterly`,
  `yearly`, `one_time`, `on_use`, or null if unknown.
- `commitment_months`: null for unknown, 0 for no minimum commitment, or a
  positive integer for a minimum term. Monthly invoices do not imply zero.
- `description`: other cited conditions specific to this option.

For example, a plan can hold both a $40/month option with monthly payments and
no minimum commitment, and a $400/year option with yearly payment and a 12-month
minimum. Exact annual charges remain primary; monthly equivalents are derived
only for display. Retain the same plan identity for both options. Never borrow
one option's evidence for another.

When converting an existing offer, submit `pricing_options`. The server clears
stored legacy prices in the same update, including when the collection is empty.
Omitting `pricing_options` preserves existing pricing. Retired price fields are
not accepted in submissions, even with null or empty values. Keep
`price_description` for shared conditions. Existing catalog data, history and
stored payloads remain readable. Never infer commitment from a legacy period.
The collection allows at most 50 options; unknown keys fail validation. Use
`/submissions/fields/` for the complete option validation schema.

## Proposed full re-research migration

When the new schema is available and a migration run is requested, inventory all
existing offers and re-research every one against current vendor sources. Build
a complete replacement set per product using the live schema, including
supported billing/payment associations. Keep an old-to-new Offer ID mapping.

Submit explicit removals of the selected old Offer IDs and creation of their
replacements in one product update. Complete validation and review before merge;
do not clear pricing upfront. Preserve product IDs, unrelated catalog data and
history. Read back each merge and reconcile every old offer to a replacement, an
explicitly reviewed removal, or an unresolved item. A failed fetch does not
establish that a plan was discontinued. This guidance does not start a
migration.
