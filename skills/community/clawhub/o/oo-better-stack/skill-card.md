## Description:

Better Stack (betterstack.com). Use this skill for ANY Better Stack request — reading, creating, updating, and deleting data. Whenever a task involves Better Stack, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use the skill to read and manage Better Stack incidents and metadata through their connected account. It provides the CLI steps and action safeguards for those tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes an unverified remote installer, and the CLI can synchronize additional agent skills.

Mitigation: Review installation before enabling the skill, use a verified CLI release, disable startup skill synchronization with OO_SKILLS_SYNC_DISABLED, and connect only the Better Stack account and permissions needed.

Risk: Write and destructive actions can change Better Stack state.

Mitigation: Confirm the exact payload and effect before write actions, and confirm the target and obtain explicit approval before destructive actions.

## Reference(s):

- [Better Stack homepage](https://betterstack.com)
- [Better Stack API documentation](https://betterstack.com/docs/errors/api/getting-api-token/)
- [oo CLI command documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-better-stack)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON]

**Output Format:** [Markdown guidance with oo CLI commands, JSON payloads, and returned data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use action-specific JSON schemas; responses include data and execution metadata.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
