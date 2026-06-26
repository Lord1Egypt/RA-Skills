## Description: <br>
Real-time operations dashboard for OpenClaw that helps install and run the dashboard while monitoring sessions, costs, cron jobs, gateway health, watchdog uptime, and dashboard API or UI changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JonathanJing](https://clawhub.ai/user/JonathanJing) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install, run, and maintain a local administrative dashboard for monitoring sessions, costs, cron jobs, watchdog status, provider health, and gateway operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard is an OpenClaw administrative control plane that can execute agent tasks and modify, reset, or update the workspace when sensitive features are enabled. <br>
Mitigation: Use a strong OPENCLAW_AUTH_TOKEN, keep the service bound to localhost unless a tunnel or proxy is tightly controlled, and enable mutating, config, provider-audit, key-loading, and restart flags only when needed. <br>
Risk: Dashboard credentials and task-spawning context can enter agent context or logs. <br>
Mitigation: Treat task spawning as sensitive, avoid placing secrets in task text, and review agent-visible payloads before using administrative actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JonathanJing/openclaw-dashboard) <br>
- [Publisher profile](https://clawhub.ai/user/JonathanJing) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [README](artifact/README.md) <br>
- [Security model](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update dashboard source files, server routes, documentation, and environment configuration for an OpenClaw deployment.] <br>

## Skill Version(s): <br>
1.7.3 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
