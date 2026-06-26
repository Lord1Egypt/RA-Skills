## Description: <br>
Provides local maintenance scripts for OpenClaw Gateway health monitoring, safe restarts, proxy switching, log cleanup, and operational notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jesson1222-ship-it](https://clawhub.ai/user/jesson1222-ship-it) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to deploy and run local OpenClaw maintenance scripts across macOS, Linux, or NAS environments. It helps monitor Gateway health, respond to proxy-related queue backlog, restart services, and clean OpenClaw logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The maintenance scripts can restart OpenClaw Gateway, switch proxy nodes, clean logs, and send Telegram notifications when configured and scheduled. <br>
Mitigation: Review and create the .env file manually, run check.sh first, and enable LaunchAgent, systemd, or cron only after accepting the operational behavior. <br>
Risk: Proxy switching depends on a configured Clash or Mihomo API and secret. <br>
Mitigation: Set CLASH_API and CLASH_SECRET explicitly, verify access to the local API, and keep the secret out of shared logs or prompts. <br>
Risk: Log cleanup deletes OpenClaw log files older than the configured retention window or larger than the configured size limit. <br>
Mitigation: Confirm the log directory and retention policy before scheduling cleanup on production machines. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jesson1222-ship-it/openclaw-maintenance) <br>
- [README.md](artifact/README.md) <br>
- [README-proxy-health.md](artifact/README-proxy-health.md) <br>
- [AGENT.md](artifact/AGENT.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local operational steps for installing, configuring, checking, and scheduling maintenance scripts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
