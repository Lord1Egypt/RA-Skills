## Description:

Manage and organize KanbanFlow board tasks by adding, moving, coloring, and deleting tasks across columns to track work progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abakermi](https://clawhub.ai/user/abakermi)

### License/Terms of Use:


## Use Case:

Developers and workflow operators use this skill to inspect KanbanFlow boards and organize tasks across columns with simple agent-mediated commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task deletion can remove KanbanFlow tasks from a board where recovery may matter.

Mitigation: Use the skill only on boards the agent is authorized to modify, and require explicit confirmation before delete commands.

## Reference(s):

- [Kanbanflow Skill on ClawHub](https://clawhub.ai/abakermi/skills/kanbanflow-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with KanbanFlow command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces board, column, task, color, movement, and deletion commands for KanbanFlow workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
