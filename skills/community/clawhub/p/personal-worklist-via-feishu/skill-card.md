## Description: <br>
Helps an agent create and manage a personal Feishu Bitable worklist, add and update tasks, configure reminders, and run worklist reviews or health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13929110463](https://clawhub.ai/user/13929110463) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual operators use this skill to maintain a Feishu-based personal work ledger, capture tasks with required fields, track status, and receive recurring work reminders. Developers or workspace administrators may use its scripts to initialize Bitable structure, configure Feishu credentials, and diagnose integration health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Feishu worklist data, Feishu/OpenClaw credentials, and recurring reminder configuration. <br>
Mitigation: Install only in trusted workspaces, confirm the Feishu app and Bitable scope before first use, and limit stored tasks to information appropriate for that workspace. <br>
Risk: The security summary says the skill can create persistent reminders and modify task, schema, or configuration state with insufficient user control. <br>
Mitigation: Review or disable automatic reminder setup before deployment, require explicit approval before running configuration-changing scripts, and audit scheduled cron entries after setup. <br>
Risk: Sensitive task details or credentials may be exposed through shared logs, examples, or configuration output. <br>
Mitigation: Avoid placing secrets or sensitive task content in shared logs and review generated examples or diagnostics before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/13929110463/personal-worklist-via-feishu) <br>
- [Publisher profile](https://clawhub.ai/user/13929110463) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Artifact examples README](examples/README.md) <br>
- [Artifact test prompts](examples/test-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured task-management guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local Node.js helper scripts that call Feishu APIs, update local configuration, and create recurring OpenClaw cron reminders.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
