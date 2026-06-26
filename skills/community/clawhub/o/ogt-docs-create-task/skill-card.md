## Description: <br>
Create and manage task documents in the docs/todo/ workflow. Use when creating new tasks, updating task status, or moving tasks between workflow stages. Provides complete task lifecycle management with verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EduardoU24](https://clawhub.ai/user/EduardoU24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to create, update, move, and verify task folders in a docs-first docs/todo workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create, update, or move task folders under docs/todo, which may change workflow state. <br>
Mitigation: Review file changes before accepting status transitions, especially moves into done, rejected, or implemented. <br>
Risk: Task completion records may be misleading if verification steps are skipped or recorded without evidence. <br>
Mitigation: Require verification.md entries with captured checks before marking tasks done or implemented. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with example file layouts and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces repository task documentation guidance and workflow state conventions; it may lead an agent to create or move files under docs/todo.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
