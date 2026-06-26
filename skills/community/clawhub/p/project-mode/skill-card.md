## Description: <br>
激活项目制多智能体开发协议。用于处理复杂的代码开发、系统搭建等需求。该工具将在后台自动拆解任务、调度程序员和测试员、更新 dev_project.md 并处理错误重试。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tincomking](https://clawhub.ai/user/tincomking) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to manage complex code development or system-building work as a staged project workflow with task decomposition, implementation, testing, integration, and delivery reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow persists project tracking state in local files, which may expose sensitive project details if secrets are stored there. <br>
Mitigation: Review dev_Project.md and system_protocol_project_mode.md before use and avoid placing secrets or credentials in project tracking files. <br>
Risk: The documented memory viewer command runs a local script outside the skill artifact. <br>
Mitigation: Run the optional memory_viewer.py command only after confirming that the local script is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tincomking/project-mode) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown status reports, task lists, code snippets, shell commands, and local project tracking file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local project tracking files under ~/.openclaw/workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
