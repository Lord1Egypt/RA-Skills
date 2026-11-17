## Description:

Checks payment-fee worksheets by recalculating expected fees, settlement amounts, totals, duplicate channels, and blank fields, with findings tied to source lines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations teams use this skill to review pasted payment-fee worksheet text for arithmetic mismatches, total-row errors, repeated payment channels, and missing key fields. It is useful before relying on channel fee and settlement figures in monthly reconciliation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles financial worksheet data and may be triggered by broad payment or reconciliation phrases.

Mitigation: Provide an explicit worksheet or table input and confirm the reported calculations before using the output for accounting decisions.

Risk: The free version intentionally omits some checks, including rate-range, negative fixed-fee, negative settlement, and threshold-based difference checks.

Mitigation: Treat the report as limited to the listed executed checks and review any checks_not_run before relying on the result.

Risk: Insufficient or malformed worksheet input can prevent meaningful conclusions.

Mitigation: Include a recognizable header row and required columns; the skill reports missing fields instead of assuming defaults or claiming no issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/payment-fee-check-free)
- [Skill definition](artifact/SKILL.md)
- [Sample input](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Console text or JSON report with findings, summary totals, executed checks, and checks not run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers when input is sufficient; insufficient input returns missing fields and advice instead of a conclusion.]

## Skill Version(s):

1.0.33 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
