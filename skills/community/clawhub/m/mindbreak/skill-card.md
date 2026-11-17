## Description:

Monitors work intensity in work-related conversations, tracks local activity timestamps, and inserts natural break reminders based on continuous work duration and time-of-day signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkxsparke](https://clawhub.ai/user/zkxsparke)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use MindBreak to add work-session break reminders to agent responses during sustained coding, writing, design, research, planning, or similar knowledge-work conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a persistent local hook that logs activity timestamps on work-related messages.

Mitigation: Install only when this local tracking is acceptable; prefer an opt-in configuration with clear controls and persistent disablement.

Risk: The skill can steer assistant replies by covertly adding break reminders and hiding that they come from a tracking hook.

Mitigation: Make reminders clearly attributed, configurable, and easy to disable so users understand why the assistant is adding them.

## Reference(s):

- [MindBreak on ClawHub](https://clawhub.ai/zkxsparke/skills/mindbreak)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown reminder paragraphs appended to agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include brief task status summaries for meal or overtime reminders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
