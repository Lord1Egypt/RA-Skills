## Description:

情感陪伴AI | AI Companion. Upload chat logs, images, or descriptions to generate companion characters that chat based on personality, remember user preferences, and evolve over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wgt9721](https://clawhub.ai/user/wgt9721)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Persona Forge to create AI companion personas from names, descriptions, chat logs, notes, and images, then run personality-driven chats with local memory, proactive reminders, optional scene images, and optional voice interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive chat logs, screenshots, images, or third-party conversations.

Mitigation: Use summaries instead of raw transcripts where possible, avoid sensitive or non-consensual content, and obtain consent before uploading conversations involving other people.

Risk: Persistent memory and relationship state may retain personal preferences and interaction history.

Mitigation: Review created state files and delete the state directory when memory should be cleared or the skill is no longer used.

Risk: Scheduled proactive messages and messaging-channel setup can continue after initial configuration.

Mitigation: Confirm channel and API setup before enabling it, and remove or disable cron jobs and channel bindings when stopping use.

## Reference(s):

- [Persona Forge ClawHub Skill Page](https://clawhub.ai/wgt9721/skills/personaforge)
- [Character Profile Template](references/character-profile-template.md)
- [Setup Guide](references/setup-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with character profile templates, JSON state examples, setup steps, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local state files, relationship state, channel configuration, and cron-based proactive message behavior.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
