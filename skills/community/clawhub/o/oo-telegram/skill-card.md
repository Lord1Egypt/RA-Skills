## Description:

Operate Telegram Bot to read, create, update, and delete data through the connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage Telegram bot chats, messages, members, invitations, and webhooks through an existing connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code and trigger automatic skill installation; the inspected artifact does not verify the remote installer or hosted connector implementation.

Mitigation: Review and install a verified CLI release separately, including its automatic skill-installation behavior.

Risk: One user-facing action may bypass its confirmation rule, and the skill exposes messaging, moderation, and deletion actions.

Mitigation: Require approval for callback notifications and messaging, moderation, and deletion; connect only the bot and permissions needed.

## Reference(s):

- [Telegram Bot API documentation](https://core.telegram.org/bots)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-telegram)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions include reads, state changes, and destructive operations; follow the skill's approval guidance.]

## Skill Version(s):

1.0.7 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
