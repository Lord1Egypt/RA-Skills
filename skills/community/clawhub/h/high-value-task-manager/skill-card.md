## Description:

高价值目标任务猎头。使用猎头筛选人才的方法论管理个人任务，通过量化分析任务价值、资源消耗与互斥关系，科学评估和动态优化任务优先级。

This skill is ready for commercial/non-commercial use.

## Publisher:

[spaceack](https://clawhub.ai/user/spaceack)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create, prioritize, update, pause, resume, complete, and review personal tasks using a value, effort, probability, urgency, and conflict model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions, schedules, and progress notes may contain sensitive personal or work information stored in a local JSON file.

Mitigation: Avoid entering secrets or highly sensitive details, and review local task files before sharing or backing up the workspace.

Risk: Chinese command phrases and generated task recommendations may be misunderstood by users who do not read Chinese.

Mitigation: Use this skill only when the operator is comfortable with the Chinese command interface and reviews task changes before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spaceack/skills/high-value-task-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/spaceack)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with command examples and JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores task data in a local JSON file under the user's OpenClaw workspace.]

## Skill Version(s):

1.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
