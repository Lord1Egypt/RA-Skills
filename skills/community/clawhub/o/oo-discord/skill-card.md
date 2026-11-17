## Description:

Operate Discord through an OOMOL-connected account to read, create, update, and delete supported data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to access supported Discord account, guild, invite, and application data through their connected OOMOL account, and to update or remove application role-connection data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run a remote CLI installer whose source and integrity were not verified.

Mitigation: Review the CLI installation separately and use a version whose source and integrity you can verify before allowing setup.

Risk: The skill documents automatic skill installation and synchronization at startup.

Mitigation: Review the CLI synchronization behavior and set OO_SKILLS_SYNC_DISABLED to disable startup synchronization when appropriate.

## Reference(s):

- [Discord API documentation](https://docs.discord.com/developers/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses and shell command instructions with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields vary by Discord action and its input schema.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
