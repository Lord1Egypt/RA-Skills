## Description:

A free deterministic checker for insurance commission and handling-fee settlement sheets that runs six row-level and sheet-level checks and cites source rows for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External insurance intermediary, agency, and bank-insurance finance teams use this skill after monthly or quarterly insurer settlement sheets arrive to check table-internal commission, handling-fee, clawback, tax, total-row, duplicate-settlement, and first-year/renewal consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Settlement sheets can contain sensitive business and financial data.

Mitigation: Run the skill only in a trusted local environment and use input tables the user is comfortable processing locally.

Risk: The free version intentionally omits cross-organization or cross-product summaries, amount-ranked handling lists, and difference attribution.

Mitigation: Review the listed checks not run before relying on the result, and use a fuller process when those omitted checks matter.

Risk: The skill checks table-internal consistency and does not determine whether commission rates, clawback timing, invoices, tax treatment, or payments are correct.

Mitigation: Treat results as arithmetic and consistency findings, then confirm contractual, regulatory, accounting, tax, and payment questions with the appropriate records or experts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/insurance-commission-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [Human-readable CLI text or JSON containing findings, summary, scope, sums, and cited source rows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite original row numbers; insufficient input returns missing requirements without drawing a conclusion.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
