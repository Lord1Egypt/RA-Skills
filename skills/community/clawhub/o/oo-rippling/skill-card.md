## Description:

Rippling (rippling.com). Use this skill for ANY Rippling request — searching and reading data. Whenever a task involves Rippling, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and administrators can use the skill to look up workers, companies, and departments in a connected Rippling account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Rippling lookup may trigger an unverified CLI installer without a clear approval step.

Mitigation: Review and approve CLI installation separately using a verified release before allowing the skill to run. Check or disable automatic agent-skill synchronization, and connect Rippling with narrowly scoped read permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-rippling)
- [Rippling](https://www.rippling.com/)
- [Rippling REST API quickstart](https://developer.rippling.com/documentation/rest-api/essentials/quickstart)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may contain employee and organizational data from the connected Rippling account.]

## Skill Version(s):

1.0.5 (source: metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
