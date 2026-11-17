## Description:

hplan provides hierarchical persistent planning for complex multi-phase tasks by creating workspace plan files and using OpenClaw memory for cross-session continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noirewinter](https://clawhub.ai/user/noirewinter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use hplan to break down complex work into phased plans, preserve task state across long sessions, and resume multi-step execution with less goal drift.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically delete a completed workspace .plan/ directory.

Mitigation: Review before installing and require explicit consent before any deletion, especially when plan files may be untracked or user-authored.

Risk: The skill persists task details to OpenClaw memory without detailed minimization controls.

Mitigation: Limit memory writes to concise, non-sensitive milestones and provide clear consent for memory writes and searches.

Risk: Broad activation on planning language may apply the workflow to tasks that do not need persistent planning.

Mitigation: Restrict activation to explicit hplan-style planning requests or ask the user before creating persistent plan state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noirewinter/skills/hplan)
- [Project homepage](https://github.com/Noirewinter/hplan)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown planning files and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates workspace planning files under .plan/ and may record concise progress details in OpenClaw memory.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
