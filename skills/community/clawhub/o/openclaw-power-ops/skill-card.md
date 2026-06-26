## Description: <br>
Operate and maintain OpenClaw installations through CLI guidance for configuration, channel and agent setup, model management, security auditing, troubleshooting, gateway administration, logs, cron, and memory commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kapslap](https://clawhub.ai/user/kapslap) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to administer OpenClaw installations, including channel setup, agent and model configuration, gateway operations, diagnostics, security audits, and routine maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides broad OpenClaw administration guidance, including delete, auto-fix, cron, gateway, credential, and memory-indexing actions. <br>
Mitigation: Require explicit user approval before executing destructive, privileged, credential-related, or broad indexing operations. <br>
Risk: Some artifact guidance is environment-specific, including Jared and root@clawdbot references. <br>
Mitigation: Remove or customize environment-specific instructions before using the skill in another OpenClaw installation. <br>
Risk: Security audits over ~/.openclaw can expose secrets or sensitive configuration details. <br>
Mitigation: Limit audit scope, redact secrets, and avoid broad scans unless the file scope is clear. <br>


## Reference(s): <br>
- [OpenClaw Power Ops release page](https://clawhub.ai/kapslap/openclaw-power-ops) <br>
- [OpenClaw CLI Cheat Sheet](references/cli-cheatsheet.md) <br>
- [OpenClaw Security Audit Reference](references/security-audit.md) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw CLI documentation](https://docs.openclaw.ai/cli) <br>
- [OpenClaw channels documentation](https://docs.openclaw.ai/cli/channels) <br>
- [OpenClaw agents documentation](https://docs.openclaw.ai/cli/agents) <br>
- [OpenClaw models documentation](https://docs.openclaw.ai/cli/models) <br>
- [OpenClaw config documentation](https://docs.openclaw.ai/cli/config) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include high-privilege operational commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
