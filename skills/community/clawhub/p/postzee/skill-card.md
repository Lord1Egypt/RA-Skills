## Description:

Generate AI images and videos, optimize prompts, create HeyGen avatar videos, and post or schedule content across 30+ social media platforms with Postzee.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasfreitas](https://clawhub.ai/user/lucasfreitas)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and social media teams use this skill to generate AI media, prepare platform-aware social content, and create or schedule posts through Postzee-connected channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure or overbroad account access when configuring Postzee.

Mitigation: Use a least-privilege Postzee credential when available, avoid sharing long-lived secrets in chat, and rotate any key that was already shared.

Risk: Unintended immediate or bulk public posting across connected social channels.

Mitigation: Require explicit review of the channel list, post content, media, schedule, and publish mode before any live or all-channel post.

## Reference(s):

- [Postzee Skill on ClawHub](https://clawhub.ai/lucasfreitas/skills/postzee)
- [Postzee Documentation](https://docs.postzee.app)
- [Postzee App](https://postzee.app)
- [Postzee Dashboard Settings](https://dashboard.postzee.app/settings)
- [Postzee Channel Connections](https://dashboard.postzee.app/channels)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands, configuration steps, and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger asynchronous media generation jobs and social posting through Postzee tools; review channel, content, media, schedule, and publish mode before publishing.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
