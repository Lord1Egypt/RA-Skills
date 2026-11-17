## Description:

Discord Bot (discord.com). Use this skill for ANY Discord Bot request — reading, creating, updating, and deleting data. Whenever a task involves Discord Bot, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to read and manage Discord resources through their connected account, including messages, channels, guild members, roles, and moderation settings. It guides the agent to inspect each action's schema and seek confirmation before changes or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute remote installation code without separate approval or integrity verification; the downloaded installer and hosted connector were not verified.

Mitigation: Review setup first; use a separately approved, pinned, verified CLI installation, review automatic skill synchronization, grant the bot only needed permissions, and require confirmation for posts, moderation, and deletions.

## Reference(s):

- [Discord Developer Documentation](https://docs.discord.com/developers/intro)
- [Discord Developer Applications](https://discord.com/developers/applications)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Discord Bot on ClawHub](https://clawhub.ai/oomol/skills/oo-discordbot)

## Skill Output:

**Output Type(s):** [API calls, Text, Shell commands, Guidance]

**Output Format:** [Text or structured Discord data, with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent is instructed to inspect action schemas; writes require confirmation and destructive actions require explicit approval.]

## Skill Version(s):

1.0.8 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
