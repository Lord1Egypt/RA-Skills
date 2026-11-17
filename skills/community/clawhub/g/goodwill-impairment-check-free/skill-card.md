## Description:

This skill runs local deterministic checks on goodwill impairment working-paper tables, recalculating totals and formula relationships and citing source evidence for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting teams use this skill before annual goodwill impairment testing or audit handoff to check exported working-paper tables for arithmetic, roll-forward, duplicate-row, and missing-field issues. It supports review preparation but does not provide accounting, tax, valuation, audit, or assurance opinions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake table-checking output for accounting, tax, audit, valuation, or assurance advice.

Mitigation: Use the skill only as a deterministic working-paper consistency check and route conclusions through qualified accounting, audit, tax, or valuation review.

Risk: A clean result may be mistaken for a complete goodwill impairment review.

Mitigation: Treat clean output as limited to the listed free checks; review omitted checks, valuation assumptions, asset-group judgments, and supporting source documents separately.

Risk: Poorly formatted or incomplete exported table text can prevent meaningful checking.

Mitigation: Provide the working-paper table with recognizable headers and data rows; when input is insufficient, the skill should report missing requirements instead of issuing a conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/goodwill-impairment-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text report or JSON findings from local command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source values; insufficient input returns missing requirements rather than a clean conclusion.]

## Skill Version(s):

1.0.22 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
