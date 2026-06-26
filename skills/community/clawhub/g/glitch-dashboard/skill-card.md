## Description: <br>
Unified web dashboard for managing task queues, monitoring system metrics, viewing ZeroTier status, and streaming recent logs in real time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris6970barbarian-hue](https://clawhub.ai/user/chris6970barbarian-hue) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use Dashboard to monitor an OpenClaw agent host, inspect queued tasks and logs, and view ZeroTier/network status from a single web UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard exposes token fragments, logs, task controls, and ZeroTier actions through a web service that binds to all network interfaces. <br>
Mitigation: Bind the service to localhost where possible, place it behind firewall or authentication controls, and avoid exposing it directly on shared or public networks. <br>
Risk: Quick install commands download remote scripts and may create persistent services with elevated privileges. <br>
Mitigation: Review installer scripts before running them, avoid piping remote scripts directly to a privileged shell, and install only in environments where the publisher and repository are trusted. <br>
Risk: Web UI actions can modify task state and leave a ZeroTier network. <br>
Mitigation: Restrict dashboard access to trusted operators and verify task/network changes before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chris6970barbarian-hue/glitch-dashboard) <br>
- [Publisher profile](https://clawhub.ai/user/chris6970barbarian-hue) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, API endpoint descriptions, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions for running and using a local web dashboard.] <br>

## Skill Version(s): <br>
2026.2.18 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
