## Description:

管理长期规划与短期待办事项。当用户提到目标、任务、计划、路线图，或需要将复杂目标拆解为存储在 memory/plans-todos.md 中的可执行项时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dawnlck](https://clawhub.ai/user/dawnlck)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to have an agent decompose goals into plans, maintain actionable todos, and update task status in a disclosed local Markdown planning file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plans and todos may contain sensitive personal details if the user asks the agent to save them.

Mitigation: Do not store passwords, keys, or highly sensitive personal details in the planning file.

Risk: Persistent task updates may save new plans or mark tasks complete before the user has reviewed the change.

Mitigation: Ask the agent to confirm before saving new plans or marking tasks complete when tighter control is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dawnlck/skills/plans)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown planning records and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains plans and todos in ~/.openclaw/workspace/memory/plans-todos.md when used by an agent with file access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
