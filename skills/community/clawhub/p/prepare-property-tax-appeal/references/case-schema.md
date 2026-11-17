# Case Data Schema (v2)

Start real work from the fail-closed `assets/case-template.json`; its human-review, appeal-ground,
residential-use, and contrary-review gates intentionally fail until verified. Use
`assets/case-example.json` only as a fictional completed example and deterministic test fixture.
Never preserve its passing attestations in a real case. Version 2 deliberately replaces the
ambiguous v1 fields `initial_assessed_value`, `requested_value`, and `likely_value_range`.

## Top-Level Objects

Required:

- `schema_version`: Exact string `2.0`
- `case`
- `selection_policy`
- `comparables`
- `rejected_comparables`
- `contrary_evidence_review`
- `sources`

## `case`

Required core fields:

- `review_title`
- `appeal_type`
- `appeal_ground`: Exact string `market_value`; the builder rejects unequal/non-uniform appraisal, exemption, classification, ownership, and other grounds that require a different evidence model
- `document_mode`: `informal_review_attachment`, `formal_board_evidence`, `protest_statement`, `grievance_support`, `abatement_support`, or `tribunal_exhibit`
- `property_address`, `apn`, and `assessment_year`
- `valuation_date` and `prepared_date`: ISO `YYYY-MM-DD`
- `value_basis`
- `likely_comparison_value_range.low` and `.high`
- `jurisdiction`
- `property`
- `valuation_rationale`
- `subject_source_ids` and `assessment_source_ids`
- `verification`

Optional narrative fields include `owner_name`, `argument_points`, `special_factors`, and `suggested_attachments`.
When present, `owner_name` must be a nonempty string or `null`; numeric and boolean stand-ins are
invalid. A provided name is rendered visibly in the shared subject table in both formats. PDF
Author metadata remains the generic `Property owner` so a name is never disclosed only through
hidden metadata.

### `case.property`

The builder is limited to residential real property. In addition to the physical fields, every
case must include `residential_use_verification` with:

- `status`: Exact string `verified_residential`; use another workflow and do not generate a packet
  when the subject is non-residential or its use has not been verified
- `classification`: The residential-use description reported by the cited parcel source
- `source_ids`: Nonempty source list that collectively includes the `parcel_record` role

This explicit, sourced verification avoids unreliable nationwide inference from free-form
`property_type` labels. `parking` and `development_or_hoa`, when present, must be nonempty strings
or `null`.

### `case.value_basis`

Required:

- `comparison_basis_kind`: Exact string `sale_comparable_market_value`; this explicit designation prevents a locally labeled appraised, assessed, or taxable amount from being compared with sales by inference
- `comparison_value_type`: `fair_market_value`, `market_value`, `just_value`, `true_value`, `actual_value`, `estimated_market_value`, or `full_cash_value`
- `comparison_value_label`: Exact human-readable jurisdiction term
- `current_comparison_value`: Positive market-oriented value to compare with sales
- `requested_comparison_value`: Positive requested amount, not above the current comparison value
- `primary_notice_value_id`: ID of the node corresponding to the value supplied by the owner
- `notice_values`: Nonempty array of sourced notice-value nodes
- `source_ids`: Must collectively include `assessment_notice` and `valuation_rule` roles

Each notice-value node requires:

- `id`: Unique 1-40 character identifier
- `value_type`: Any comparison category plus `appraised_value`, `assessed_value`, `equalized_assessed_value`, `state_equalized_value`, `limited_property_value`, or `taxable_value`
- `label` and `authority`: Exact notice term and taxing/assessing authority
- `current_value`: Nonnegative amount, including zero when the official record supports it
- `requested_value`: Nonnegative amount or `null` when the authority must recalculate it
- `source_ids`: Must include `assessment_notice`
- `derivation.kind`: `same_as_source`, `ratio`, `cap`, `equalization`, `exemption`, `classification`, `authority_specific`, or `reported_only`
- `derivation.source_value_id`: `comparison_value` or another notice-node ID
- `derivation.factor`: Positive number only for `ratio`; otherwise `null`
- `derivation.description`: Case-specific explanation of the transformation
- `derivation.source_ids`: Must include `valuation_rule`

The builder rejects cycles and transformations outside its directed type matrix.
`same_as_source` requires the same value type and amount. `ratio` converts a market-value source
to an appraised, assessed, or limited-property target; it also supports sourced
`appraised_value -> assessed_value` and `limited_property_value -> assessed_value` chains such as
Arizona's statutory assessment percentage. A ratio uses a factor no greater than 1 and must
reconcile mechanically within normal rounding tolerance. `cap` runs from market value to an
appraised/assessed category, from appraised to assessed or limited value, or from assessed to
limited value; it cannot run backward. `classification` runs from market value to appraised or
assessed value. `equalization` runs from an assessed category to an equalized category, or from
equalized assessed value to state-equalized value. `exemption` and `authority_specific` can reduce
an assessed/equalized value to taxable value; authority-specific taxable-to-taxable links are also
allowed. Caps, classifications, exemptions, and authority-specific transformations cannot increase
either the current or requested amount. Use `reported_only` when the source reports both values but
no supported mechanical relationship is known. For every other derivation kind, a child
`requested_value` must remain `null` when its source `requested_value` is `null`.
Every non-null notice-node `requested_value` must also be no greater than that node's own
`current_value`; an appeal packet cannot silently request an increase in an assessed or taxable
notice value.

### `case.verification`

Each boolean must be set to `true` only after the named human check is complete:

- `official_rules_rechecked`
- `subject_facts_reconciled`
- `value_basis_reconciled`
- `comparable_sales_verified`
- `contrary_evidence_reviewed`

`official_rules_current_as_of` must be an ISO date equal to `case.prepared_date`. These are preparer attestations; the script cannot independently prove that a source is authentic or legally controlling.

### `case.jurisdiction`

Required:

- `country`: `US`
- `state` and `state_code`, including `DC`
- `county_or_locality`
- `route_family`: one documented in `appeal-routes.md`
- `appeal_stage`, `filing_authority`, and `valuation_standard`
- `filing_deadline`: fixed ISO date or `null`
- `filing_deadline_rule`
- `official_form_required`, `official_form_name`, and `official_form_url`
- `submission_url`
- `informal_preserves_formal_deadline`: `true`, `false`, or `null`
- `source_ids`: Must collectively include `appeal_rule`, `submission_rule`, and `valuation_rule`
- `deadline_source_ids`: Must include `deadline_rule`

The route must match the state registry. A verified local exception requires `route_override.reason` and sourced `route_override.source_ids` with `appeal_rule` role. A fixed deadline before `prepared_date` is rejected.
`official_form_name` and `official_form_url` must be `null` when absent. When present, the name
must be a nonempty string and the URL must satisfy the canonical public-HTTPS rules, even when an
official form is not required for the current stage.

### Declaration Fields

- `declaration`: `null` by default; otherwise exact owner-reviewed text
- `declaration_owner_approved`: Strict boolean, default `false`
- `include_signature_block`: Strict boolean, default `false`

A declaration is rendered only when approval is exactly `true`. Signature lines require an approved declaration. Strings such as `"false"` are invalid.

## `selection_policy`

- `strict_bed_bath_match`
- `strict_property_type_match`
- `exclude_above_current_comparison_value`: Advocacy-table filter applied only after neutral candidate review
- `allow_provisional_range_prices`
- `minimum_comps` and `maximum_comps`
- `legal_sale_window.start_date` and `.end_date`
- `legal_sale_window.basis`
- `legal_sale_window.source_ids`: Must include `sale_window_rule`

The v1 `max_post_valuation_days` shortcut is rejected because no universal nationwide post-valuation window exists.

## `comparables`

Required for every selected comparable:

- `address`, `apn`, `transaction_id`, `sale_date`, and `sale_price`; `sale_price` must be stated in whole dollars, and `transaction_id` must be a stable recorder instrument, deed, MLS transaction, or equivalent source record identifier
- `price_source_kind`: `exact_closed_price` or `range_lower_bound`
- `property_type`, `bedrooms`, `bathrooms`, and `living_area_sqft`
- `arm_length_status`: Must be `verified` or `likely`
- `relevance`
- `source_ids`: Must collectively include `parcel_record` and `transaction_record`

Recommended:

- `same_development`, `distance_miles`, and `year_built`
- `reported_price_range.low` and `.high` when using `range_lower_bound`; both endpoints must be stated in whole dollars, and `sale_price` must equal `.low`

The builder computes price per square foot. A provisional lower endpoint is labeled as such and is never described as exact consideration. Range evidence is treated as an interval; only exact prices enter a median, and at least two exact prices are required before a central point statistic is printed.

## `rejected_comparables`

Record every plausible candidate omitted after neutral review. Required:

- The same normalized `address`, `apn`, `transaction_id`, `sale_date`, `sale_price`, `price_source_kind`, `property_type`, `bedrooms`, `bathrooms`, `living_area_sqft`, `relevance`, and `source_ids` fields used for selected comparables
- `valuation_status`: `valuation_eligible_omitted` or `research_only_inadmissible`
- `reasons`: Nonempty standardized-reason list
- `relevance_review`: Specific comparison with the subject and selected set
- `materially_contrary`: Strict boolean
- `source_ids`: Valuation-eligible rows must collectively include `parcel_record` and
  `transaction_record`; every research-only row requires `parcel_record`, with reason-specific
  transaction-source rules described below

Recommended physical and transaction fields are also the same as selected comparables.
`valuation_eligible_omitted` rows must remain inside the sourced legal sale window, have verified
or likely arm's-length status, and participate in neutral-pool arithmetic. A
`research_only_inadmissible` row remains in the audit ledger but is excluded from every anchor,
interval count, span, and median. It must use at least one inadmissibility reason and set
`materially_contrary` to `false`. An inadmissibility label is not sufficient by itself: the row
facts must support the reason. `non_arm_length` and `non_market_transfer` require
`arm_length_status: not_arm_length`; `outside_legal_sale_window` requires a date actually outside
the sourced window; and `unverified_transaction` requires unknown arm's-length status, a
provisional range, a `parcel_record` source, and no source claiming the `transaction_record` role.
Non-arm's-length, non-market, out-of-window, and duplicate reasons require both parcel and
transaction-record sources. `duplicate_record` requires `duplicate_of_transaction_id`; it must
reference the same earlier `transaction_id`, and the address, APN, sale date, price kind,
whole-dollar price, and whole-dollar range must match exactly. A repeated APN with a different
transaction ID or transaction facts is a distinct sale, not a duplicate. Allowed reasons are:

- `above_current_comparison_value`
- `bed_bath_mismatch`
- `living_area_mismatch`
- `age_mismatch`
- `location_mismatch`
- `condition_mismatch`
- `hoa_context_mismatch`
- `property_type_mismatch`
- `non_arm_length`
- `non_market_transfer`
- `unverified_transaction`
- `outside_legal_sale_window`
- `duplicate_record`

## `contrary_evidence_review`

Required:

- `completed`: Must be `true`
- `all_plausible_candidates_recorded`: Must be `true`
- `summary`: Neutral description of higher and otherwise contrary evidence reviewed
- `source_ids`: Must collectively include `parcel_record` and `transaction_record`
- `disclosure`: Required when any rejected comparable has `materially_contrary: true`; otherwise nullable

The builder applies one relevance score to selected and valuation-eligible omitted candidates. If
an eligible omitted candidate scores at least as highly as the best selected candidate,
`materially_contrary` must be `true` and disclosure is mandatory. Eligible omitted candidates
participate in neutral-pool interval arithmetic; research-only inadmissible rows never do.
All candidates tied for the highest score are rendered as co-best candidates in a deterministic
transaction-identity order independent of advocacy-table status.

## `sources`

Each source requires:

- `id`: 1-40 letters, digits, dots, underscores, or hyphens
- `source_kind`: `public_url` or `owner_attachment`
- `title` and `publisher`: Safe descriptive text, never a file path or private locator
- `url`: A canonical public `https` URL for `public_url`; exactly `null` for `owner_attachment`
- `accessed_date`: ISO date no later than `prepared_date`; this is the review date for an owner attachment
- `supports`: Nonempty fact list
- `roles`: Nonempty typed-role list

An `owner_attachment` represents a notice, report, letter, MLS closed-sale sheet, closing
disclosure, or other evidence the owner supplied without copying its contents, local path, portal
URL, signed link, or another private locator into the case JSON. It may use only
`assessment_notice`, `marketability_evidence`, and `transaction_record` roles. A private
`transaction_record` may establish the closed-sale facts for a selected or valuation-eligible
omitted comparable, but that row must also cite a separate public `parcel_record`. The output uses
a fixed label stating that the attachment is not embedded and must be filed separately.
`owner_attachment` cannot establish parcel/residential classification, valuation transformations,
appeal rules, sale windows, deadlines, or submission requirements; those roles continue to require
public sources. Unknown fields are rejected throughout the case schema so a locator cannot be
hidden in an ad hoc `local_path` or similar property.

Allowed roles:

- `appeal_rule`
- `assessment_notice`
- `deadline_rule`
- `marketability_evidence`
- `parcel_record`
- `sale_window_rule`
- `submission_rule`
- `transaction_record`
- `valuation_rule`

Public URLs with embedded credentials, query strings, fragments, control characters, backslashes,
percent-encoded authorities, malformed or lowercase percent escapes, encoded unreserved path
characters, noncanonical Unicode/IDNA authorities, raw non-ASCII paths, IANA special-use domains,
or non-public-unicast IP forms are rejected. This includes browser-compatible short and integer
IPv4 forms, Unicode dot separators, fullwidth digits, IANA special-purpose IPv4/IPv6 ranges,
multicast, transition addresses, and local NAT64 forms. The policy uses frozen address tables so
results do not change with the Python interpreter's `ipaddress` version. The builder never fetches
URLs. Separate research tooling must use an SSRF-protected connector or resolve once, pin the
connection to a validated numeric address while preserving SNI and `Host`, verify the peer, and
repeat that process for every redirect. A preflight lookup followed by an ordinary second DNS
resolution is not sufficient. For private owner documents, use `owner_attachment` with `url: null`,
a locator-free title and fact description, and attach the actual document separately through the
official filing channel.

The CLI reads at most 5 MiB of UTF-8 case JSON and rejects nesting deeper than 100 containers
before parsing. Duplicate object keys and Unicode surrogate code points are rejected instead of
being accepted into an output-bound structure. Selected comparables are capped at 20, rejected
candidates at 100, sources at 200, and `selection_policy.maximum_comps` at 20. Validation reports
at most 200 detailed errors plus one suppression summary. Malformed, oversized, ambiguous, and
recursively nested inputs return bounded errors without a traceback.
