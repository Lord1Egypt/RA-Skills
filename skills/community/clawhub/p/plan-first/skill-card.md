## Description:

Plan First helps agents solve complex multi-step tasks by generating, validating, and executing a detailed plan before acting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncatbot](https://clawhub.ai/user/simoncatbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, analysts, and project planners use this skill to break complex work into ordered steps with dependencies, verification criteria, risk analysis, and rollback guidance before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: For sensitive work such as production migrations, user data processing, moderation systems, or deployments, planning output could be mistaken for approval to proceed.

Mitigation: Keep normal authorization, privacy, backup, access-control, and review procedures in place before acting on the plan.

Risk: Broad activation can add unnecessary planning overhead for simple, direct, or exploratory tasks.

Mitigation: Apply the skill to multi-step tasks with dependencies, and skip it for single-step questions or unconstrained brainstorming.

## Reference(s):

- [Plan First detailed examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown plan with task, ordered steps, verification, risk analysis, and rollback sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task-specific file, tool, command, and rollback notes when relevant.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
