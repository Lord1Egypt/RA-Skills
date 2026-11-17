## Description:

Task Planner helps users manage personal tasks and schedules with natural-language commands for reminders, recurring tasks, updates, deletion, and Markdown calendar export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luzewen](https://clawhub.ai/user/luzewen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage personal tasks, schedules, reminders, recurring commitments, and calendar exports through an OpenClaw assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task details and reminder logs may be stored as plaintext files in the user's home directory.

Mitigation: Avoid highly sensitive task titles or notes, and review generated files and permissions before relying on the skill.

Risk: Voice transcription can send audio to OpenAI when transcription is used.

Mitigation: Use transcription only with appropriate consent and avoid recording sensitive audio.

Risk: Reminder automation may run from cron or another scheduler.

Mitigation: Review scheduler entries and command paths before enabling reminders.

## Reference(s):

- [Server-resolved source repository](https://github.com/luzewen/openclaw-task-planner)
- [ClawHub skill page](https://clawhub.ai/luzewen/skills/liuxiaoying-task-planner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Natural-language guidance, JSON command results, reminder text, and Markdown calendar files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create plaintext task, reminder log, and calendar files in the user's home directory.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 4.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
