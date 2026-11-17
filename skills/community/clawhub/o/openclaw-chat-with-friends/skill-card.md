## Description:

Helps users set up a shared Telegram channel so different OpenClaw bots can chat together with friends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moon-frost](https://clawhub.ai/user/moon-frost)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to configure a shared Telegram channel, add multiple OpenClaw bots, connect each bot, and set conversation rules for controlled multi-bot interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bots added as Telegram channel administrators can read channel messages and may expose private conversation content.

Mitigation: Use a dedicated private channel, add only intended participants and bots, grant the minimum permissions needed, and get participant consent before connecting bots.

Risk: Forwarding channel messages to third-party Telegram helper bots to obtain a Chat ID can disclose private content or channel metadata.

Mitigation: Prefer OpenClaw-supported channel detection or Telegram Bot API methods under the user's control; avoid sending real private messages to helper bots.

Risk: Multiple bots in one channel can trigger reply loops or excessive posting.

Mitigation: Configure name prefixes, direct-mention triggers, cooldowns, and persistent AGENTS.md rules before allowing bots to converse freely.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moon-frost/skills/openclaw-chat-with-friends)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with configuration steps and troubleshooting notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides users through Telegram channel setup, bot permissions, OpenClaw channel binding, and persistent conversation rules.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
