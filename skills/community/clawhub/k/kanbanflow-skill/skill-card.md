## Description: <br>
Manage and organize KanbanFlow board tasks by adding, moving, coloring, and deleting tasks across columns to track work progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abakermi](https://clawhub.ai/user/abakermi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators can use this skill to ask an agent for KanbanFlow command guidance that lists boards, columns, and tasks and changes task state when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward KanbanFlow task changes, including deletion. <br>
Mitigation: Require confirmation before delete or other task-changing commands are executed. <br>
Risk: Commands depend on the local kanbanflow command or integration being trusted and connected to the intended board. <br>
Mitigation: Verify the local command or integration before using the skill to operate on KanbanFlow tasks. <br>


## Reference(s): <br>
- [Kanbanflow Skill on ClawHub](https://clawhub.ai/abakermi/kanbanflow-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Text or Markdown with KanbanFlow command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task-changing commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
