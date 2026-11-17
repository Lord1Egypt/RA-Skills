## Description:

n8n (n8n.io). Use this skill for ANY n8n request — reading, creating, updating, and deleting data. Whenever a task involves n8n, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and n8n workspace operators use this skill to inspect workflows, executions, tags, variables, and data tables, and to make approved changes through their connected n8n account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs unverified remote code, and the deployed connector was not verified.

Mitigation: Review the setup before installing and use a reviewed, pinned CLI release; account for OOMOL-mediated access by using a narrowly scoped n8n connection.

Risk: The CLI may synchronize additional agent skills at startup.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 for each CLI invocation to disable startup skill synchronization.

Risk: Write and deletion actions can change or remove n8n data.

Mitigation: Keep the documented approval step for each write or deletion and confirm its exact target and effect before execution.

## Reference(s):

- [n8n API documentation](https://docs.n8n.io/api/api-reference/)
- [n8n](https://n8n.io)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-n8n)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [Schema-guided CLI commands and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read, update, create, activate, archive, or delete n8n resources, subject to the documented approval requirements.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
