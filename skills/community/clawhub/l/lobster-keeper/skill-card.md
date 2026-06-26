## Description: <br>
自动执行日常维护：状态检查、自我复盘、记忆流动、任务记录。基于龙虾饲养员的六条经验。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ayadododo](https://clawhub.ai/user/Ayadododo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to run recurring workspace maintenance: checking identity, memory, logs, available skills, and producing a concise status report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read workspace identity, user, memory, and log files during maintenance. <br>
Mitigation: Install and run it only in workspaces where that access is acceptable. <br>
Risk: Scheduled runs or broad write and execution permissions could apply changes without immediate review. <br>
Mitigation: Enable scheduled execution and write or exec tools only after reviewing the workspace contents and resulting maintenance changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ayadododo/lobster-keeper) <br>
- [Publisher profile](https://clawhub.ai/user/Ayadododo) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown status reports and maintenance guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read workspace identity, memory, and log files and may write maintenance records when the runtime grants those tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
