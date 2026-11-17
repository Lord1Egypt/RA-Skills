## Description:

独立思考四部曲。触发场景：开口/动手前需要深度思考时、方案决策前、复盘总结时、任何需要依托向量补全记忆做全局判断的场景。与沟通四部曲并行通用，贯穿对话、做事、学习、复盘全流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[markma84](https://clawhub.ai/user/markma84)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill as a structured thinking, decision, and retrospective workflow that consults a local vector-memory system before communication or action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on unaudited local vector-memory scripts and databases.

Mitigation: Use only after reviewing and trusting the referenced local scripts and storage location.

Risk: Task summaries or sensitive work context may be stored for future retrieval.

Mitigation: Require explicit user approval before writing memory, limit stored content, and define retention boundaries.

Risk: The skill broadly asks agents to apply this memory workflow across routine tasks.

Mitigation: Narrow use to opt-in situations where vector recall is necessary and appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/markma84/skills/independent-thinking-4steps)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown guidance with inline shell command examples and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts the agent to retrieve and persist task context through user-local vector-memory scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
