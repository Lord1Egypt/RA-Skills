## Description:

待办清单 is a lightweight to-do helper for adding tasks by voice or text, marking and deleting tasks, sorting by priority, tracking progress, and persisting tasks in local JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain lightweight personal or project task lists with priorities, completion status, due dates, and progress summaries stored locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Importing or running the documented helper can unexpectedly create or modify the local quick_tasks.json file.

Mitigation: Review the code before use and move example operations behind an explicit main guard or into a separate example file.

Risk: Delete and complete operations permanently change local task state.

Mitigation: Use the skill only on local task data and review task IDs before applying destructive or completion actions.

Risk: Task IDs are based on current list length and may be reused after deletion.

Mitigation: Use unique or monotonic task IDs before relying on the data for persistent workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-quick-todo)
- [Publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify a local quick_tasks.json task file when the documented Python helper is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
