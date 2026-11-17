## Description:

Perdoo (perdoo.com). Use this skill for ANY Perdoo request — reading, creating, and updating data. Whenever a task involves Perdoo, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected Perdoo account can read Perdoo data and create or update goals, key results, KPIs, and progress updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified downloaded code, and automatic agent-skill synchronization may install additional skills without review.

Mitigation: Install a verified CLI release before enabling the skill, and review or disable automatic agent-skill synchronization.

Risk: A connected Perdoo account permits operations that can change data.

Mitigation: Use appropriate account permissions and review write payloads before running them.

## Reference(s):

- [Perdoo](https://www.perdoo.com)
- [Perdoo API documentation](https://api-docs.perdoo.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON request payloads and structured result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Perdoo data returned by read actions and write-action results]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
