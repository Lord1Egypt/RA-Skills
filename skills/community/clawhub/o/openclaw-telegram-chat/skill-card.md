## Description:

Guides OpenClaw users through Telegram group onboarding, cross-instance bot messaging, mentions, identity mapping, and personal Telegram bot setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and maintainers use this skill to set up Telegram-based communication between agent instances, map bots to user identities, and troubleshoot mentions and message delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires handling a Telegram bot token, which can expose bot access if copied into shared files or repositories.

Mitigation: Use a dedicated bot token, keep it out of committed configuration, and rotate it if it is exposed.

Risk: Broad Telegram bot access can allow the bot to observe more group activity than users expect.

Mitigation: Restrict allowed_chats, grant only the minimum Telegram permissions needed, and avoid administrator status unless it is required.

Risk: Group participants may not understand what messages a configured bot can see or relay.

Mitigation: Keep privacy mode enabled where possible and make group participants aware of the bot's visibility before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adminlove520/skills/openclaw-telegram-chat)
- [Artifact README](artifact/README.md)
- [Artifact SKILL guide](artifact/SKILL.md)
- [Telegram BotFather](https://t.me/BotFather)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guide with Telegram commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no executable scripts are included.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact changelog lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
