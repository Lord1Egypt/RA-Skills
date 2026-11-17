## Description:

Checks prepaid-card consumption reconciliation tables by recomputing row balances, recognized income, totals, duplicates, and missing fields, with source evidence for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and cashiering teams use this skill during monthly closing, reconciliation, or inventory checks to validate prepaid-card consumption tables. It performs deterministic local checks and reports missing input instead of making unsupported conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat reconciliation findings as complete accounting, tax, or legal advice.

Mitigation: Use the output as a local reconciliation aid and have qualified finance or accounting staff review decisions that affect reporting, tax, or refunds.

Risk: The free release intentionally omits some checks that are listed as outside this package.

Mitigation: Review the withheld checks before relying on the result, and perform those checks manually or with the complete product when they matter.

Risk: Inputs can contain sensitive prepaid-card or member reconciliation data.

Mitigation: Run the checker in a controlled local environment and avoid sharing input files or outputs beyond the people who need them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/prepaid-card-consumption-check-free)
- [Skill definition](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Human-readable text or JSON produced by a local Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows and evidence; insufficient input returns missing requirements without a reconciliation conclusion.]

## Skill Version(s):

1.0.45 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
