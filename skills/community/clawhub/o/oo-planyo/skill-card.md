## Description:

Planyo (planyo.com). Use this skill for ANY Planyo request — searching and reading data. Whenever a task involves Planyo, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to retrieve Planyo site and resource information through an OOMOL-connected Planyo account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A missing oo CLI dependency can trigger unverified remote code installation without an explicit approval step.

Mitigation: Review the CLI installation, prefer an independently verified version-pinned install, require approval before setup commands, and check whether installation changes other agent skills.

Risk: Planyo access passes through OOMOL.

Mitigation: Understand that access path before enabling the skill.

## Reference(s):

- [Planyo](https://www.planyo.com/)
- [Planyo API documentation](https://www.planyo.com/api.php)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured Planyo response data with text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Data is limited to the available read actions and connected account access.]

## Skill Version(s):

1.0.1 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
