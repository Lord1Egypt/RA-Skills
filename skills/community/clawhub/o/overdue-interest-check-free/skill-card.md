## Description:

Checks overdue-interest worksheets for recalculation errors, day-count mismatches, total-row discrepancies, duplicate customers, and blank fields, with findings tied to source lines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, legal, and collections staff use this local checker before month-end close, demand letters, or litigation preparation to review overdue-interest worksheets for arithmetic and table-consistency issues. It supports arithmetic review only and does not provide legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake worksheet arithmetic review for legal advice about debt validity, limitation periods, enforceability, or court outcomes.

Mitigation: Treat outputs as table-review findings only and route legal questions to qualified legal review.

Risk: The free version explicitly omits checks for judicial rate caps, date anomalies, non-positive principal or rates, and negative interest.

Mitigation: Use an additional review process or a fuller checker when those conditions affect the decision.

Risk: The checker depends on pasted text with recognizable table headers and does not read .xlsx files directly.

Mitigation: Confirm the copied text matches the source spreadsheet and includes the required headers before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/overdue-interest-check-free)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and optional JSON results from the local Node.js checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source lines; insufficient input returns missing fields instead of a pass/fail conclusion.]

## Skill Version(s):

1.0.35 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
