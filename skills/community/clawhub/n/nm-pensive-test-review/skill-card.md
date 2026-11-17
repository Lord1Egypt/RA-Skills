## Description:

Evaluates test suites for coverage gaps, TDD/BDD compliance, and anti-patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review test suites before releases or after test failures. It helps identify framework constraints, coverage gaps, weak scenarios, and concrete test improvement actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One scanner reported incomplete coverage because three local references could not be resolved.

Mitigation: Review the skill and the unresolved references before installation, accounting for the scanner coverage gap.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown test review with framework findings, coverage gaps, quality issues, and a remediation plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are tied to test behavior and should include source locations and evidence where available.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
