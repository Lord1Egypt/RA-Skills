## Description: <br>
Comprehensive Mission Control dashboard for OpenClaw - monitor agents, automation, teams, documents, messages, and system metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Broedkrummen](https://clawhub.ai/user/Broedkrummen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to run and manage a Mission Control dashboard for monitoring agents, messaging, task execution, automation workflows, documents, alerts, SLOs, and system metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard can expose remote mission-control capabilities without clearly documented access controls or safety boundaries. <br>
Mitigation: Keep it localhost-only unless the application source, authentication model, Tailnet ACLs, per-agent permissions, and approval controls have been reviewed. <br>
Risk: The documented setup includes persistent services and a Tailscale proxy that may run with elevated privileges. <br>
Mitigation: Avoid running the proxy as root where possible, and confirm how to stop, disable, and remove the mission-control and Tailscale services before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Broedkrummen/overkill-mission-control) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides operational instructions for a local OpenClaw Mission Control dashboard.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
