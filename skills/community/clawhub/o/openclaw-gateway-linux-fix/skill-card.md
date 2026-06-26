## Description: <br>
Fix and diagnose OpenClaw Gateway service issues on Linux, including incorrect gateway service status, user-scope systemd bus errors, safe restarts, shell escalation environment issues, and reboot persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maksmirnnov](https://clawhub.ai/user/maksmirnnov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to troubleshoot and repair OpenClaw Gateway service behavior on Linux systems. It focuses on user-scope systemd configuration, safe service restart sequencing, SSH and sudo environment issues, and persistence across logout or reboot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes state-changing Linux commands that can edit the OpenClaw Gateway systemd user service and change restart behavior. <br>
Mitigation: Review each command before running it, back up the service unit before editing, and confirm the target service and user context. <br>
Risk: Restarting the gateway can terminate the active agent process before follow-up checks run. <br>
Mitigation: Schedule any continuation or notification before triggering the restart and avoid chaining status checks after the restart command. <br>
Risk: Restart context files and Telegram notifications can expose operational details if they include sensitive data. <br>
Mitigation: Keep sensitive values out of temporary context files and notifications, and confirm the intended Telegram recipient before announcing. <br>
Risk: Enabling linger and service auto-start changes persistence across logout or reboot. <br>
Mitigation: Use linger and service enablement only when persistent gateway operation is intended for that host. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maksmirnnov/openclaw-gateway-linux-fix) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/maksmirnnov) <br>
- [Diagnosis Checklist](references/diagnosis.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes diagnostic checks and state-changing Linux service commands for user review before execution.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
