## Description:

Checks project billing and collection ledgers by recalculating line items and totals, detecting duplicates, blanks, and negative amounts, and citing source rows for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, accounting, and project operations teams use this skill during monthly close, reconciliation, and billing reviews to check project billing and collection ledgers. It helps recalculate ledger relationships, surface missing or duplicate entries, and explain what source rows support each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the free checker as a complete billing and collections audit even though it intentionally omits several listed checks.

Mitigation: Review the omitted-check list before relying on results, and use another review process or the complete offering for checks outside the free scope.

Risk: Incomplete or ambiguous ledger input can produce no conclusion or make findings difficult to interpret.

Mitigation: Provide the full table with clear headers and review the cited source rows and missing-input messages before acting on findings.

Risk: The tool processes project billing and collection ledger text that may contain sensitive commercial data.

Mitigation: Run it only in a controlled local environment where local Node.js execution on that data is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/project-billing-collection-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable text or JSON results from a local Node.js ledger checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; insufficient input returns missing requirements instead of a conclusion.]

## Skill Version(s):

1.0.52 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
