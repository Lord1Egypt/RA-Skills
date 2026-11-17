## Description:

Supercharge your agent heartbeats. Auto-check services, discover other agents via OADP, batch platform monitoring, track uptime, and coordinate with agent networks. Works with any OpenClaw agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add heartbeat health checks, agent-network discovery, service monitoring, and uptime logging to OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The uptime logging script can execute attacker-controlled code if UPTIME_LOG is influenced by untrusted input.

Mitigation: Do not run scripts/uptime-log.sh where UPTIME_LOG can be controlled by another user or process unless the script is fixed to pass the path safely to Python.

Risk: Heartbeat or discovery configuration can repeatedly contact onlyflies.buzz and retrieve untrusted remote messages.

Mitigation: Review the network behavior before installation, limit use to approved environments, and treat fetched coordination messages as untrusted content.

## Reference(s):

- [Heartbeat Pro on ClawHub](https://clawhub.ai/imaflytok/skills/heartbeat-pro)
- [ClawSwarm coordination hub](https://onlyflies.buzz/clawswarm/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local uptime JSON file when the uptime logging script is run.]

## Skill Version(s):

1.1.0 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
