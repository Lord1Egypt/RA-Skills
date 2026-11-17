## Description:

Overkill Mission Control is a comprehensive OpenClaw dashboard for monitoring agents, automation, teams, documents, messages, system metrics, real-time activity, task execution, and enterprise-level operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[broedkrummen](https://clawhub.ai/user/broedkrummen)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to set up and operate a mission-control dashboard for agent monitoring, messaging, task execution, automation workflows, document management, alerts, SLOs, and system health review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent system services, including a root-level Tailscale proxy service.

Mitigation: Review service units, required privileges, logs, and uninstall or disable steps before installation.

Risk: The dashboard can expose an agent-control interface over Tailscale.

Mitigation: Keep access local until Tailscale ACLs, authentication, allowed users, and logging are confirmed.

Risk: The skill documents autonomous execution and polling endpoints for agent messages and tasks.

Mitigation: Review endpoint behavior and restrict network access before enabling message polling or task execution.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/broedkrummen/skills/overkill-mission-control)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash commands and systemd configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local dashboard startup guidance, service configuration, Tailscale exposure steps, and troubleshooting commands.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
