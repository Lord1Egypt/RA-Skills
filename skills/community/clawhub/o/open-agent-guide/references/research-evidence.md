# Research evidence for catalog submissions

## Text-only review

Review assesses supplied text. It does not inspect images or perform optical
character recognition. Publisher-supplied image accessibility text, including
alt text and accessible labels, and captions can support explicit claims. Check
official ownership, product scope, surrounding text, and qualifications. An
official product badge labeled "SOC 2 Type II" or "HIPAA compliant" can support
vendor self-attestation without a separate report or certificate. Unrelated
customer logos and frameworks offered to customers do not establish the
product's compliance. Preserve the source URL and distinguish accessibility text
and captions from surrounding prose. Do not infer details absent from text.

Accessibility text may differ from the image. Review accepts this risk and does
not verify visual agreement. Image-only exceptions and contradictions can go
unseen.

## Cite textual support

Cite accessible authoritative text for each claim. If support requires
inspecting an image, use existing research routes and budgets to find textual
support. Leave the field unresolved if that support is unavailable. Do not use
an unverified transcription as corroboration. Do not infer absence from excluded
images.

## Record support before drafting

Read the live writable-field schema and product coverage guidance before
research. Use the field definitions to interpret each proposed value.

For each factual field, record the field path, proposed value, source URL,
product or component, applicable plan, and material qualifications. Read the
source before drafting. Accurate paraphrases are allowed. A source can support
several structured values without a separate exact quotation for each value.
Preserve conditions such as opt-in settings, regional limits, billing periods,
and plan eligibility. Keep unresolved or unsupported values unset.

Use excerpts to explain support when useful. Record uncertainty and incomplete
inspection in the research notes. Do not infer facts from prior knowledge,
navigation labels, or an unrelated product from the same publisher. Put evidence
URLs and justification in the submission-level description. Keep catalog copy
focused on the product.

## Interpret deterministic pointer checks

Maintainer preview-research records can include deterministic pointer checks. A
`structurally_valid` result confirms document structure only. Assess product
identity, official ownership, scope, and contradictions before drafting. Reuse
the saved preview text only within its recorded freshness and evidence scope.
These records do not contain completed semantic assessments or supported
patches.

## Apply documented citation exemptions

Citation exemptions depend on the entity and field. Slugs and subject names are
identifiers. An Offer's product reference is a catalog relationship identifier;
the source does not need to print its UUID. Offer display names are exempt, but
prices, billing terms and eligibility still need evidence for that product and
plan. Factual assertions in descriptions still need sources, even when the
surrounding wording is a neutral summary.

Typed pointers supply their own citation and must satisfy the documented
reachability, content-kind and applicability checks. Do not extend an exemption
to every URL, enum, boolean, or relationship. A new publisher assignment needs
evidence for the publisher relationship. Use the live schema and field guidance
for entity-specific requirements.

For a confirmed absence, inspect the authoritative page class for that field.
Preserve the product scope and material qualifications in the attestation. Page
silence requires sufficiently complete evidence. A failed fetch, clipped
excerpt, or page about another capability cannot establish absence. Leave the
value unknown when the required evidence is unavailable.

## Handle a source size failure

Read the failure to identify the affected operation: source retrieval, preview
delivery, local evidence preparation, or model assessment. Record the source
URL, capture hash, measured size, limit and unit when available. Record missing
diagnostics as unknown.

Keep the field unresolved when required evidence cannot be processed. Do not
infer absence or wrong content from a size failure. Do not clip the source or
remove qualifications to fit a limit. A focused official source can replace the
source only when it preserves the evidence needed for the same claim and scope.

Do not repeat the same failed processing operation with unchanged evidence and
configuration. Record the correction before another attempt. A fresh retrieval
can establish that the source changed; it does not guarantee that the next
operation can process it. Contact <support@openagentguide.com> when the preview
cannot return a required source. The current preview interface does not provide
a submitter artifact-download fallback.

## Inspect feedback before repair

Read lifecycle state, review feedback, check results and curator resolution that
the server makes available. A passed `FACT_CHECK` means evidence preparation
completed. Neither that check nor `review_ready` establishes approval or
application. Preserve the existing repair budget and predecessor submission
identity.

Correct the proposed value or its supporting evidence according to the reported
reason. Keep support for every retained factual field. If feedback is missing,
record that limitation instead of inventing a reviewer rationale. Historical
quotation diagnostics describe old records and do not define current evidence
requirements.

A source preview and a later review can capture different content. Preserve
capture times and hashes when available. Do not present preview coordinates as
references to a later review's evidence. The server owns evidence preparation,
source-reference integrity and semantic judgment.

### Semantic research replay

Maintainer semantic-checker artifacts can record local supported, contradicted,
or insufficient-evidence outcomes for frozen previews. These artifacts do not
change the submission contract. Continue the normal source-review and submission
workflow until a harness integration validates fresh inputs and immutable draft
fragments. A local supported assessment does not authorize a catalog claim.
