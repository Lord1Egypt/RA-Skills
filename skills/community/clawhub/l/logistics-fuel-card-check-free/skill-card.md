## Description:

A local fleet fuel-card checker that recomputes card balances, L/100km consumption, fuel amount consistency, total rows, duplicate fueling, mileage rollback, and missing fields, with findings tied to source line numbers and vehicle plates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Fleet administrators and finance teams use this skill during monthly fuel-card settlement to recheck spreadsheet arithmetic, duplicate fueling entries, mileage consistency, and fuel-consumption outliers before reimbursement, driver review, or cost accounting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker validates table arithmetic and consistency, not oil-station receipts, fuel-card systems, GPS records, tax treatment, or other external evidence.

Mitigation: Treat findings as spreadsheet-review evidence and reconcile material issues against authoritative source systems before audit, payment, or disciplinary action.

Risk: Missing columns or incomplete input prevent a reliable conclusion.

Mitigation: Provide a complete table with headers and treat insufficient-input results as no conclusion rather than as a clean review.

Risk: Fleet fuel-card data may contain sensitive operational or employee information.

Mitigation: Use the skill only with data approved for local processing and minimize or redact unnecessary identifiers before running checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/logistics-fuel-card-check-free)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Plain text or JSON result containing executed checks, scope, findings, summary, and insufficient-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers and vehicle plates; the skill reports when material is insufficient instead of producing a clean conclusion.]

## Skill Version(s):

1.0.5 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
