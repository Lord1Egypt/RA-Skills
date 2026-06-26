## Description: <br>
禅道(ZenTao) MCP大模型能力扩展包。提供跨项目的数据聚合视图、一句话生成任务、无缝报工(Log Effort)、自动状态流转等四组原生能力。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenish](https://clawhub.ai/user/chenish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Project managers, team leads, and development teams use this skill to let an agent query ZenTao work items, summarize team status, create or update tasks, log effort, and prepare standup or weekly-report material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires password-backed access to ZenTao. <br>
Mitigation: Use a least-privileged ZenTao account and avoid placing passwords directly in shell commands. <br>
Risk: The skill can let an agent change live tasks, bugs, stories, effort logs, assignees, statuses, and estimates. <br>
Mitigation: Require the assistant to show the exact task, bug, story, iteration, assignee, status, and effort changes before executing any write action. <br>
Risk: The server security verdict is suspicious for this release. <br>
Mitigation: Review or pin the npm package before installation and deploy only after local security review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenish/mcp-zentao-pro) <br>
- [chenish publisher profile](https://clawhub.ai/user/chenish) <br>
- [@chenish/zentao-mcp-agent npm package](https://www.npmjs.com/package/@chenish/zentao-mcp-agent) <br>
- [mcp-zentao-pro GitHub issues](https://github.com/chenish/mcp-zentao-pro/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with CLI command examples and agent tool-use guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ZenTao entity IDs, assignees, statuses, estimates, deadlines, dashboard summaries, and proposed write actions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
