## Description: <br>
待办清单是一项轻量任务管理技能，支持语音或文字添加任务、完成和删除任务、优先级排序、进度统计以及本地 JSON 存储。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals, teams, and agents use this skill to maintain lightweight local task lists, including daily todos, shopping lists, project steps, and GTD-style task tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or update a local quick_tasks.json file and can mark or delete todo items. <br>
Mitigation: Review requested task changes before executing generated add, complete, or delete commands, and keep the JSON file in an expected local skill directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-quick-todo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples plus JSON task data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores task data locally in quick_tasks.json when the implementation is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
