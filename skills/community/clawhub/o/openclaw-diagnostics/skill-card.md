## Description: <br>
Diagnoses and troubleshoots OpenClaw config, channel, group message, cron job, and authentication issues using logs and a built-in knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cooperun](https://clawhub.ai/user/Cooperun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw configuration, channel, group messaging, cron, and authentication problems. It gathers local status, config, and recent logs, checks common failure patterns, and returns troubleshooting guidance grounded in bundled OpenClaw documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic commands can print local OpenClaw configuration and logs that may contain tokens, account IDs, private messages, or channel details. <br>
Mitigation: Review and redact diagnostic output before sharing it, and run the skill only in environments where local OpenClaw diagnostics are acceptable. <br>
Risk: Bundled documentation, logs, and diagnostic data may be mistaken for operational instructions. <br>
Mitigation: Treat bundled docs and collected logs as troubleshooting evidence, then verify suggested fixes against the active OpenClaw configuration before applying changes. <br>


## Reference(s): <br>
- [OpenClaw Diagnostics Skill](https://clawhub.ai/Cooperun/openclaw-diagnostics) <br>
- [OpenClaw Common Issues Diagnostic Rules](references/common-issues.md) <br>
- [OpenClaw Knowledge Base Index](references/knowledge-base-index.md) <br>
- [OpenClaw Auth Monitoring](https://docs.openclaw.ai/automation/auth-monitoring) <br>
- [OpenClaw Cron Jobs](https://docs.openclaw.ai/automation/cron-jobs) <br>
- [OpenClaw Automation Troubleshooting](https://docs.openclaw.ai/automation/troubleshooting) <br>
- [OpenClaw Group Messages](https://docs.openclaw.ai/channels/group-messages) <br>
- [OpenClaw Channel Routing](https://docs.openclaw.ai/channels/channel-routing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with shell command suggestions, diagnostic checklists, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include references to local config, status, and log output that should be redacted before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
