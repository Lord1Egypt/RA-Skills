## Description: <br>
Long Task Monitor coordinates Worker and Monitor agents so long-running OpenClaw tasks can be tracked through hook-logger logs and 10-minute Announce reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scotthuang](https://clawhub.ai/user/scotthuang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage long-running tasks while a Monitor agent watches Worker progress, records status, and reports completion, failure, or stalled activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on hook-logger and reads local OpenClaw logs, which may expose sensitive task or session information. <br>
Mitigation: Install only if the hook-logger dependency is trusted, avoid tasks that may write secrets to logs, and review logged content before sharing artifacts. <br>
Risk: The skill can store task/session metadata and control Worker sessions with broad local authority. <br>
Mitigation: Manually verify session cleanup after completion and delete old long-task folders when they are no longer needed. <br>
Risk: Monitor behavior requires shell execution to write monitoring records. <br>
Mitigation: Review generated commands before execution and run the skill only in workspaces where the agent is permitted to write monitoring files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/scotthuang/long-task-monitor) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Long Task Monitor Plan](artifact/long-task-monitor-plan.md) <br>
- [Monitor Agent Prompt](artifact/monitor-prompt.txt) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, JSON files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON task/status records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OpenClaw task folders and hook-logger logs to track Worker and Monitor session state.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact metadata and changelog list 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
