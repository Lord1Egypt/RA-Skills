## Description: <br>
A general TODO management skill that records active tasks and completed work separately from daily journal notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AxelHu](https://clawhub.ai/user/AxelHu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to keep concise local TODO and DONE task records, update task status as work starts or finishes, and review current progress without mixing task state into daily logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task text is stored locally in TODO.md and DONE.md and may include sensitive work details if users add them. <br>
Mitigation: Avoid recording sensitive tasks unless local storage is acceptable, and review the memory/todo files before sharing or publishing workspace contents. <br>


## Reference(s): <br>
- [TODO List Detailed Specification](references/spec.md) <br>
- [TODO.md Example](references/example-todo.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/AxelHu/openclaw-todo-list) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown task entries and concise guidance with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local memory/todo/TODO.md and memory/todo/DONE.md files when used for task tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
