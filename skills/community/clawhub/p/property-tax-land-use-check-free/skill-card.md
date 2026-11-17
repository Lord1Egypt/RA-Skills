## Description:

This skill locally checks Chinese property tax and urban land-use tax worksheets by recalculating declared amounts, reconciling reported and book tax, and citing source line numbers for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and tax staff at companies with Chinese property or land holdings use this skill before filing to check property tax and urban land-use tax worksheet arithmetic, installment amounts, declared tax, and book-tax reconciliation. It provides local worksheet checks and missing-data signals, not tax advice or policy selection.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The worksheet content may contain sensitive business tax and accounting data.

Mitigation: Run the skill only in an environment where local Node execution over that worksheet data is acceptable; server security evidence found no network use, persistence, credential access, or hidden behavior.

Risk: The skill does not validate local policy choices, deduction ratios, land grade rates, exemptions, or source accounting values.

Mitigation: Confirm those policy and source-data inputs separately before filing; treat the skill as a worksheet consistency checker, not tax advice.

Risk: Incomplete or unrecognized worksheet input can prevent reliable conclusions.

Mitigation: Provide the full table header and detail rows, then review any missing-field or not-concluded output instead of treating silence as a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/property-tax-land-use-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable console output or structured JSON findings with source line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally over user-provided worksheet text; insufficient input produces missing-field guidance rather than a pass or fail conclusion.]

## Skill Version(s):

1.0.55 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
