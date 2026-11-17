## Description:

上下文窗口优化器 helps agents compress long conversation history by removing redundancy, preserving key decisions and task state, and producing a concise context summary for long sessions, multi-file work, and larger projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent users use this skill to turn long-running conversations into compact summaries that retain decisions, requirements, current progress, open tasks, user preferences, and key file paths. It is intended for sessions where token growth, repeated dialogue, or stale process detail makes active context harder to use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A compressed summary could omit safety constraints, approvals, requirements, open tasks, or key file paths from an active session.

Mitigation: Ask the agent to show the proposed summary and explicitly preserve safety constraints, requirements, approvals, open tasks, and key file paths before using it.

Risk: Replacing the full transcript before review can make it harder to recover omitted context.

Mitigation: Keep the original conversation available until the proposed compressed context has been reviewed and explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-context-opt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown context optimization report and concise summary guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; users should review summaries before replacing active conversation history.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
