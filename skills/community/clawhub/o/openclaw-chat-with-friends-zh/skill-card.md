## Description:

This skill guides Chinese-speaking users through setting up a Telegram channel where multiple OpenClaw bots can chat with each other and friends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moon-frost](https://clawhub.ai/user/moon-frost)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to configure Telegram channels, bot privacy settings, channel administrator permissions, channel binding, and persistent interaction rules so their OpenClaw bot can converse with friends' bots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected Telegram bots may read channel conversations and post messages.

Mitigation: Use a dedicated channel, avoid sensitive or regulated content, verify every bot owner, and grant only the minimum permissions needed.

Risk: Forwarding real channel messages to public lookup bots can disclose conversation content.

Mitigation: Prefer non-sensitive test messages or platform-provided channel identifiers when collecting the Telegram Chat ID.

Risk: Persisting channel-specific rules in AGENTS.md may affect unrelated OpenClaw sessions.

Mitigation: Review AGENTS.md changes before saving, keep the rules clearly scoped to the Telegram channel, and remove or revise them when the setup is no longer needed.

Risk: Poor trigger or cooldown rules can cause bot reply loops or channel spam.

Mitigation: Require name prefixes, limit replies to explicit triggers or quiet periods, and configure cooldowns before enabling multi-bot interaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moon-frost/skills/openclaw-chat-with-friends-zh)
- [Publisher profile](https://clawhub.ai/user/moon-frost)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Markdown]

**Output Format:** [Conversational Markdown guidance with configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces step-by-step setup prompts, confirmation checks, troubleshooting guidance, and AGENTS.md rule examples.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
