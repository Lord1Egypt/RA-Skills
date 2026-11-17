## Description:

Breathe (breathehr.com). Use this skill for ANY Breathe request — searching and reading data. Whenever a task involves Breathe, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Breathe account can ask an agent to retrieve account details, employee records, departments, and locations through Breathe read actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unverified software with broader effects on the agent's installed skills.

Mitigation: Review and install the CLI separately before use. Use the documented OO_SKILLS_SYNC_DISABLED setting to prevent automatic skill synchronization when appropriate.

Risk: The connected Breathe account can expose employee data to OOMOL.

Mitigation: Connect only the intended Breathe account and consider OOMOL's access to employee data.

## Reference(s):

- [Breathe skill release](https://clawhub.ai/oomol/skills/oo-breathe)
- [Breathe homepage](https://www.breathehr.com/)
- [Breathe API documentation](https://developer.breathehr.com/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON data with natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Breathe account, employee, department, and location information.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
