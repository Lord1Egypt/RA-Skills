## Description:

Mio智能聊天 is a Chinese-language chat helper that learns local habit signals, detects idle states, starts proactive conversations, and classifies task-like requests for delegation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[libaiqwq](https://clawhub.ai/user/libaiqwq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to provide Chinese-language companion chat, lightweight habit-aware idle detection, and task-intent routing to sub-agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Habit learning can retain local chat-time, active-hour, topic, and mood-pattern history.

Mitigation: Review or clear artifact/data/habits.json and disable habitLearning or freeDetection if local habit retention is not desired.

Risk: Proactive chat and intent routing can activate unexpectedly or treat casual language as a task.

Mitigation: Narrow triggers and disable taskDistribution or proactive settings when unexpected activation or delegation would be disruptive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/libaiqwq/skills/mio-smart-chat)
- [Publisher profile](https://clawhub.ai/user/libaiqwq)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Chinese-language text responses with structured task, status, and initiation data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store local habit and task data when habit learning or task distribution is enabled.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
