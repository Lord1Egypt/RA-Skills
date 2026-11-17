## Description:

Set up a new OpenClaw agent end to end, including requirement gathering, Discord bot setup, OpenClaw configuration, Mission Control registration, heartbeat scheduling, optional OneDrive access, and final verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boltth](https://clawhub.ai/user/boltth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to onboard a new agent with Discord routing, Mission Control registration, heartbeat automation, optional shared storage access, and final operational checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks operators to handle a Discord bot token and store it locally.

Mitigation: Protect or externalize the token, restrict file access, and rotate or revoke the bot token if exposure is suspected.

Risk: The runbook creates durable automation through cron and heartbeat configuration.

Mitigation: Require explicit approval before adding scheduled jobs and document how to remove cron entries, heartbeat state, memory entries, and bot access.

Risk: Agent IDs, roles, and routing values are used in shell commands and configuration edits.

Mitigation: Validate agent IDs, roles, and channel identifiers before using them in commands or writing OpenClaw configuration.

Risk: Optional OneDrive access can expose shared files beyond the new agent's intended scope.

Mitigation: Grant only the requested libraries, verify symlink targets, and confirm the new agent creates files only in its assigned subfolder.

## Reference(s):

- [New Agent Setup checklist](references/checklist.md)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [ClawHub skill page](https://clawhub.ai/boltth/skills/new-agent-setup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown runbook with inline JSON, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires operator-provided agent identity, Discord bot details, channel ID, and optional OneDrive access choices.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
