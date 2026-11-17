## Description:

Life Scheduler gives an AI agent a persistent fictional daily life state by generating outfits, schedules, moods, and current activity context for persona and roleplay use cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t-chen-cn](https://clawhub.ai/user/t-chen-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make persona, companion, roleplay, virtual idol, or game NPC agents maintain a believable daily state across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates ongoing background state that may read persona files and recent-chat context.

Mitigation: Set reference_recent_chats to 0 when recent-chat use is unnecessary, and periodically review or clean HEARTBEAT.md and memory/life-history/.

Risk: Scheduled generation, archive writes, context injection, and configuration edits can persist generated roleplay content into later conversations.

Mitigation: Require confirmation before enabling or changing cron jobs, bootstrapFiles, HEARTBEAT.md writes, archive behavior, context injection, or config changes.

Risk: Generated fictional daily state may be mistaken for factual memory or user-provided information.

Mitigation: Keep generated content clearly scoped to the agent persona and review injected HEARTBEAT.md content before relying on it in sensitive contexts.

## Reference(s):

- [Life Scheduler ClawHub Page](https://clawhub.ai/t-chen-cn/skills/life-scheduler)
- [Configuration Guide](references/CONFIGURATION.md)
- [Configuration Examples](references/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown daily-state content with JSON configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates HEARTBEAT.md, may archive historical daily states under memory/life-history/, and may inject the generated state into future agent context.]

## Skill Version(s):

1.1.0 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
