## Description:

Helps OpenClaw manage interleaved conversation threads by prioritizing a mainline, parking side topics, assigning weights, and periodically steering attention back to the highest-value task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucaszh7](https://clawhub.ai/user/lucaszh7)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to keep one noisy chat organized into weighted threads, protect the active mainline, and resume important work after interruptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update local Markdown files that summarize conversation threads and priorities.

Mitigation: Review generated task-weight-manager files, avoid storing sensitive transcript details, and disable persistence when file-backed summaries are not wanted.

Risk: Optional HEARTBEAT, cron, memory, session, or external LLM helper integrations can increase automation, token cost, and transcript-processing exposure.

Mitigation: Enable optional automation only through explicit user choice, keep intervals conservative, and limit transcript scope to the minimum needed for re-prioritization.

## Reference(s):

- [OpenClaw Integration Notes](artifact/references/integration.md)
- [Usage Patterns](artifact/references/usage-patterns.md)
- [Project homepage](https://github.com/LucasZH7/openclaw-task-weight-manager)
- [ClawHub skill page](https://clawhub.ai/lucaszh7/skills/openclaw-task-weight-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status blocks, concise prose, and optional workspace Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update task-weight-manager/threads.md, task-weight-manager/decisions.md, and HEARTBEAT.md when workspace file access is available.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
