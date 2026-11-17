## Description:

Send messages to Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to send Discord messages from scripted workflows and communication tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package references scripts/discord_bot.py, but that script is not included in the artifact.

Mitigation: Verify the intended bot implementation before installation or execution.

Risk: The skill can post content to Discord using a bot token.

Mitigation: Use a least-privileged Discord bot token and avoid sending sensitive or private content.

Risk: The trigger guidance is broad for a message-posting skill.

Mitigation: Use the skill only for explicit Discord posting tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-discord-bot)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DISCORD_API_KEY and references a Discord bot script that is not included in the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
