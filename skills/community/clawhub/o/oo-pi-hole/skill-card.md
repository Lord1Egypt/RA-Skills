## Description:

Pi-hole (pi-hole.net). Use this skill for ANY Pi-hole request — reading, creating, updating, and deleting data. Whenever a task involves Pi-hole, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Pi-hole administrators and users can inspect DNS activity and configuration, manage clients, groups, domains, and lists, and control blocking through the oo CLI. Confirm the exact effect before running actions that change or remove Pi-hole data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installation may run downloaded installer code that was not inspected in this release review.

Mitigation: Review and approve the CLI installation separately before using the skill.

Risk: Setup may synchronize additional agent skills without clearly explaining those changes.

Mitigation: Review any skills added during setup; use OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization.

Risk: Using the connected service gives OOMOL access to Pi-hole credentials and DNS activity.

Mitigation: Use the connection only if you trust OOMOL with that access, and retain the documented confirmations before changes or destructive actions.

## Reference(s):

- [Pi-hole homepage](https://pi-hole.net)
- [Pi-hole API documentation](https://docs.pi-hole.net/api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Pi-hole skill release](https://clawhub.ai/oomol/skills/oo-pi-hole)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Text]

**Output Format:** [JSON payloads sent through the oo CLI and structured connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
