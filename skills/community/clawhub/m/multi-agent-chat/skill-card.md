## Description:

Prevent common failures in multi-agent Discord conversations where multiple AI agents are chatting in the same channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to coordinate multi-bot Discord channels, townhalls, group discussions, and collaborative sessions. It provides behavioral rules that reduce duplicate responses, reaction spam, rate-limit collisions, token waste, and looped bot-to-bot exchanges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may affect conversation quality in channels that are English-only or human-only because it includes multi-bot coordination behavior and a fixed Korean fallback phrase.

Mitigation: Install it only in channels where multiple bots are expected to coordinate, and review the fallback language before deployment.

Risk: Discord reaction events and repeated bot-to-bot replies can waste tokens or contribute to loops in multi-agent channels.

Mitigation: Disable reaction notifications for bot channels, keep replies short, enforce turn-taking, and require human input after repeated exchanges.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Configuration]

**Output Format:** [Markdown with YAML configuration snippet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides concise operating rules, alert conditions, and a Discord reaction notification setting.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
