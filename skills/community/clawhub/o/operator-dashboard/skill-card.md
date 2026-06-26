## Description: <br>
Zero-config OpenClaw gateway monitoring that runs health checks, sends daily concise summaries, alerts on critical issues, and offers fixes only with approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukeaustin13](https://clawhub.ai/user/lukeaustin13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor an OpenClaw gateway, cron jobs, plugins, disk, memory, and sessions from the active conversation channel. It provides concise status summaries, critical alerts, and approval-gated operational fix suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose cleanup, restart, retry, reinstall, or deletion actions that affect local OpenClaw services or files. <br>
Mitigation: Require exact-command confirmation before approving any fix action, and verify the result after execution. <br>
Risk: Scheduled summaries and critical alerts can send operational status into the active conversation channel. <br>
Mitigation: Review the channel before enabling scheduled reports and keep immediate alerts limited to disclosed critical conditions. <br>


## Reference(s): <br>
- [Operator Dashboard on ClawHub](https://clawhub.ai/lukeaustin13/operator-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise Markdown status messages with inline shell commands for proposed fixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily summaries are limited to 5-6 lines; destructive or service-impacting actions require explicit approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, artifact metadata, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
