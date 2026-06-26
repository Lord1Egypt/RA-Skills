## Description: <br>
高价值目标任务猎头使用猎头筛选人才的方法论管理个人任务，通过量化分析任务价值、资源消耗与互斥关系，帮助用户评估并动态优化任务优先级。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spaceack](https://clawhub.ai/user/spaceack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create, update, rank, pause, resume, and complete personal tasks in Chinese using command triggers such as 挖坑 and 填坑. It supports prioritization based on expected value, success probability, time, energy cost, urgency, and conflict checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task names, deadlines, notes, tags, and progress history are stored locally as plaintext JSON. <br>
Mitigation: Avoid entering secrets or highly sensitive plans, and protect or delete the task file when the history is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spaceack/high-value-task-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown task summaries with JSON task records and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores task data as local plaintext JSON under ~/.openclaw/workspace/memory/tasks/tasks.json.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
