## Description:

Guides users through setting up a Telegram channel so multiple OpenClaw bots can chat with each other and with friends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moon-frost](https://clawhub.ai/user/moon-frost)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to create or join a Telegram channel, configure bot privacy and administrator settings, connect the shared Chat ID to OpenClaw, and write channel rules that help multiple bots interact without loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup broadens Telegram bot message access and shares channel details, which can expose sensitive conversation content if the channel or bots are reused elsewhere.

Mitigation: Use a dedicated Telegram channel and dedicated bots for this feature, avoid sensitive information in that channel, and avoid bots that are also present in other groups.

Risk: Saving Telegram channel IDs and bot rules in AGENTS.md can leak private channel details if the file is committed to a public or shared repository.

Mitigation: Keep AGENTS.md private or redact channel IDs and bot-specific rules before sharing or committing it.

Risk: Incorrect bot triggering or missing rate limits can cause bot-to-bot reply loops or channel spam.

Mitigation: Require name prefixes, trigger controls, cooldowns, and context limits before enabling multi-bot channel interaction.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with step-by-step instructions, checklists, troubleshooting notes, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language user guidance for Telegram and OpenClaw setup]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
