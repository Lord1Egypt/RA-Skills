## Description:

物业公共收益公示与分成核对（免费版） locally checks residential community public-income ledgers by recalculating owner-share amounts, quarterly subtotals, grand totals, duplicate registrations, missing fields, invalid ratios, and negative amounts with source line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External property-management teams, owner committees, and auditors use this skill to check community public-income ledgers before quarterly disclosure or annual review. It helps identify arithmetic and ledger-entry issues in owner-share calculations and posted totals, while leaving legal compliance and paid-scope checks out of scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive financial or property-management ledger records.

Mitigation: Use it only with ledger files the user intends to analyze and keep execution local as described by the security evidence.

Risk: The free version omits compliance, repair-fund, arrears, and prioritized remediation checks.

Mitigation: Treat results as arithmetic and ledger-consistency checks only, and do not rely on them as complete legal, audit, or compliance conclusions.

Risk: Materials that are missing headers or required rows can prevent reliable conclusions.

Mitigation: Provide the ledger with recognizable headers and detail rows; when materials are insufficient, the skill reports what is missing instead of returning a pass finding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/property-public-income-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON results with finding categories, source line numbers, summaries, executed checks, and checks not run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard libraries; accepts a user-provided ledger file or sample input.]

## Skill Version(s):

1.0.52 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
