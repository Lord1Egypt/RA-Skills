## Description:

Configure a Discord bot as an OpenClaw message channel with token setup, server authorization, permissions, and slash command support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to connect an OpenClaw assistant to Discord by creating a bot, inviting it to a server, configuring credentials, and enabling channel or slash-command interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discord bot credentials and OpenClaw configuration can expose access to the connected assistant if shared or stored insecurely.

Mitigation: Keep the bot token and ~/.openclaw/config.yaml private, use environment variables where practical, and rotate the token if exposure is suspected.

Risk: Messages visible to the Discord bot may be processed by the configured AI backend.

Mitigation: Limit the bot to trusted servers and channels, restrict allowed guild IDs, and enable direct messages only when needed.

## Reference(s):

- [Discord Developer Applications](https://discord.com/developers/applications)
- [Openclaw Discord Setup on ClawHub](https://clawhub.ai/yang1002378395-cmyk/skills/openclaw-discord-setup)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup steps, configuration examples, troubleshooting notes, security guidance, and cost information.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
