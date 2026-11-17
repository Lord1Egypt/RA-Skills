## Description:

Connects a local LM Studio model directly to Discord as a lightweight chat bot that bypasses the OpenClaw gateway for lower-latency CPU-only setups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dq-stack](https://clawhub.ai/user/dq-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and server operators use this skill to create a minimal Discord.js bot that forwards messages from a configured guild to a local LM Studio chat completions endpoint. It is suited to lightweight Discord chat deployments where low latency matters and tool access, conversation memory, slash commands, and multi-model orchestration are not needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bot processes messages broadly in the configured guild.

Mitigation: Run it only where members know messages are processed by an LLM bot, and restrict handling to mentions, commands, or approved channels.

Risk: The template places the Discord token in source configuration.

Mitigation: Move the token to an environment variable or secret store before use.

Risk: Message and reply content may be logged.

Mitigation: Disable content logging by default or redact message text from logs.

Risk: Default setup may use broad dependencies and bot permissions.

Mitigation: Pin dependencies and reduce Discord bot permissions to the minimum required for the intended channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dq-stack/skills/lm-studio-discord)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord bot authorization URL template](https://discord.com/oauth2/authorize?client_id=BOT_CLIENT_ID&permissions=1024&scope=bot)
- [Bot template](scripts/bot-template.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a Discord.js bot template configured for a local LM Studio chat completions endpoint.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
