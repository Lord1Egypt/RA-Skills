## Description:

Pad Mode turns messy or complex requests into structured, trackable execution plans with task breakdown, approval gates, progress tracking, and delivery review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yipxiyi](https://clawhub.ai/user/yipxiyi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to plan and execute non-trivial work through explicit planning, discussion, approval, tracked execution, and final review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plan files may retain secrets or sensitive business details provided in user requests.

Mitigation: Avoid including secrets or sensitive details in plan requests unless those details are appropriate to save in OpenClaw plan files.

Risk: Background or sub-agent execution can carry out approved plans with less continuous user attention.

Mitigation: Use background or sub-agent execution only after reviewing and approving the plan and execution mode.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yipxiyi/skills/pad-mode)
- [README](artifact/README.md)
- [Plan Template](artifact/assets/plan-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown plan documents, progress updates, execution summaries, and task-specific guidance or commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates resumable plan files and may coordinate foreground or background execution after user approval.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
