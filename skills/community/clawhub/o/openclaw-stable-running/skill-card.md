## Description: <br>
Provides operational guidance, scripts, and configuration examples for keeping an OpenClaw gateway running continuously with process supervision, health checks, restart handling, resume patterns, resource cleanup, and logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foxyy1126](https://clawhub.ai/user/foxyy1126) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw for unattended service operation, including systemd or PM2 supervision, health checks, restart behavior, task-resume patterns, cleanup, and log monitoring. It is intended for teams that want a practical operational runbook and helper scripts for long-running OpenClaw deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended persistence can keep OpenClaw running after logout or reboot and may restart failed processes automatically. <br>
Mitigation: Install only when unattended operation is intended, review each systemd, PM2, and cron command before use, and monitor restart logs for repeated failures. <br>
Risk: The network monitor can make host-level default-route changes when connectivity checks fail. <br>
Mitigation: Avoid scripts/network_monitor.sh unless failover is explicitly required, and test with interface validation, dry-run procedures, rollback steps, and administrator approval. <br>
Risk: Operational scripts and examples reference sensitive OpenClaw environment and data paths. <br>
Mitigation: Protect /home/openclaw/.openclaw/.env and /home/openclaw/data with least-privilege file permissions and review backup, logging, and cleanup behavior before deployment. <br>


## Reference(s): <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Task resume reference](references/task-resume.md) <br>
- [ClawHub release page](https://clawhub.ai/foxyy1126/openclaw-stable-running) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, JavaScript, YAML, and service configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes helper scripts for health checks, cleanup, PM2 process configuration, and network monitoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
