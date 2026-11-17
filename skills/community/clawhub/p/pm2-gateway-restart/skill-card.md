## Description:

Use PM2 to reliably restart the OpenClaw gateway on Windows, including recovery paths for port conflicts, crashed gateway processes, FIN_WAIT_2 TCP delays, and scheduled task failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zitao666](https://clawhub.ai/user/zitao666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to restart, inspect, and recover a Windows OpenClaw gateway managed by PM2. It is aimed at local gateway maintenance where standard OpenClaw gateway start and stop commands are unreliable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restart and reinstall commands can interrupt a running OpenClaw gateway.

Mitigation: Confirm downtime impact, check PM2 status, and choose a maintenance window before running production restart or reinstall commands.

Risk: Installing PM2 globally introduces package-version and supply-chain exposure.

Mitigation: Pin and review the PM2 package version where practical and install from trusted npm configuration.

Risk: Gateway management commands can modify local service state and may require elevated Windows shell access.

Mitigation: Avoid elevated shells unless required and verify the target gateway process and port before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zitao666/skills/pm2-gateway-restart)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target a local Windows OpenClaw gateway process managed by PM2.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
