## Description:

Runs a local monthly manufacturing self-check covering production yield and scrap, material usage and loss, and inventory weighted-average cost reconciliations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations staff at manufacturing companies use this skill during month-end close, reconciliation, and inventory review to check pasted segmented tables for arithmetic, totals, duplicates, blanks, and missing-input conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill can falsely appear to have no issues when required check sections are missing or fewer than three sections run.

Mitigation: Treat missing_section, insufficient_input, or sections_done below 3 as inconclusive and request complete input before relying on results.

Risk: The skill performs local arithmetic and reconciliation checks and does not replace accounting judgment, assurance, or formal filings.

Mitigation: Review results against source records and route accounting decisions through the user's normal qualified review process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/manufacturing-monthly-selfcheck-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON check results with cited findings and missing-input messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on pasted text or JSON input; reports withheld checks and treats insufficient input as inconclusive.]

## Skill Version(s):

1.0.49 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
