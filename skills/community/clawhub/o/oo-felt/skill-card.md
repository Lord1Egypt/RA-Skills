## Description:

Felt (felt.com). Use this skill for ANY Felt request — reading, creating, updating, and deleting data. Whenever a task involves Felt, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to inspect Felt projects and maps and to create, update, move, duplicate, or delete them through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can execute unverified remote code and may install other agent skills, introducing broader agent changes.

Mitigation: Review and approve CLI installation separately before enabling the skill; use the documented OO_SKILLS_SYNC_DISABLED=1 setting to disable startup skill synchronization when appropriate.

Risk: Felt write and destructive actions can change or delete user data.

Mitigation: Keep the skill's approval requirements for write and destructive actions, and confirm the exact target and effect before execution.

## Reference(s):

- [Felt REST API documentation](https://developers.felt.com/rest-api/getting-started)
- [Felt homepage](https://felt.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-felt)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read or change Felt data; write and destructive actions require user approval.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
