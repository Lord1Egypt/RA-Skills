## Description: <br>
Self-healing watchdog for the OpenClaw gateway that backs up openclaw.json, checks gateway health, restarts failed processes, and rolls back to the last known good config on failure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install and manage a local OpenClaw gateway watchdog that backs up configuration, restarts failed gateway processes, and rolls back bad configs after failed health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog can restart the OpenClaw gateway and replace ~/.openclaw/openclaw.json from backup. <br>
Mitigation: Review the setup script before installing, keep an independent config backup, and confirm the installed cron, launchd, or systemd entry after setup. <br>
Risk: The systemd example runs the watchdog as root. <br>
Mitigation: Avoid the root systemd example unless that privilege is required, and prefer the least-privileged service account that can manage the gateway. <br>
Risk: Automatic rollback may replace a current config with an older backup after a failed health check. <br>
Mitigation: Inspect watchdog logs and preserved broken config files before relying on rollback behavior for incident recovery. <br>


## Reference(s): <br>
- [Docker Self-Healing Setup](references/docker.md) <br>
- [macOS LaunchDaemon](references/launchd.md) <br>
- [Systemd Service](references/systemd.md) <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/gw-self-heal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local setup and status scripts for cron, launchd, systemd, or Docker watchdog flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
