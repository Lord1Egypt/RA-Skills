## Description: <br>
Manage and inspect the OpenClaw multi-agent gateway by listing agents, checking model health, viewing routing rules, managing crons, inspecting context budgets, and running system diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atiati82](https://clawhub.ai/user/atiati82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and administer an OpenClaw gateway, including agent inventory, model status, routing, scheduled jobs, triggers, context budgets, and health diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad OpenClaw gateway administration, including persistent routing, cron, trigger, prompt, and gateway configuration changes. <br>
Mitigation: Require an explicit diff and approval before edits to ROUTING.json, CRONS.json, TRIGGERS.json, agent prompt files, or openclaw.json, and keep a backup or rollback path. <br>
Risk: The skill references local diagnostic and restart commands that may execute workspace-specific scripts or processes. <br>
Mitigation: Inspect status.sh and verify any npx restart command before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run local inspection commands and may guide changes to gateway configuration files when approved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
