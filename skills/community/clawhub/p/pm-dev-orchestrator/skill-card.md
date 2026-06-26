## Description: <br>
This skill orchestrates a PM bot and one or more Dev bots in a private Telegram group so strict commands can install ClawHub skills and manage OpenClaw cron jobs on a Dev OpenClaw server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kiril-Shturman](https://clawhub.ai/user/Kiril-Shturman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to coordinate a planner bot and executor bot in a private Telegram group for installing ClawHub skills and managing OpenClaw cron jobs through strict chat commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram chat commands can trigger high-impact actions such as skill installation and scheduled agent job changes. <br>
Mitigation: Use only in a tightly controlled private setup and require human approval before installs or cron changes. <br>
Risk: Unauthorized messages could be executed if Telegram chat.id and from.id checks are not enforced in the active execution path. <br>
Mitigation: Enforce the configured group chat id and PM bot from.id before parsing or executing any DEV command. <br>
Risk: A compromised or overly broad skill source could install untrusted capabilities on the Dev server. <br>
Mitigation: Restrict allowed skill publishers or slugs and review each requested install before execution. <br>
Risk: Cron jobs can persist unattended agent behavior after creation. <br>
Mitigation: Default new cron jobs to disabled or expiring until reviewed and explicitly enabled. <br>
Risk: The Dev bot token can grant Telegram access if exposed. <br>
Mitigation: Store the Dev bot token only in protected configuration and never print secrets in chat responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Kiril-Shturman/pm-dev-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with JSON, shell command, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a Dev-side parser and executor scaffold for allowlisted skill and cron commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
