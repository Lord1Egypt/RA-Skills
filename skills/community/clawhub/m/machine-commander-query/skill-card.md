## Description:

MachineCommander queries a MachineCommander MCP service for real-time construction machine and vessel data, including status, locations, alerts, projects, and trajectories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sandofree](https://clawhub.ai/user/sandofree)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to ask natural-language questions about construction machinery and vessels in active projects, including counts, location distribution, operational status, fuel-related information, alerts, and historical tracks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents a machine-management command that could affect real equipment if the connected MCP service permits command execution.

Mitigation: Use only a trusted, access-controlled MachineCommander MCP service and require explicit human authorization before any real equipment command is issued.

Risk: Location, tenant, project, alert, and trajectory responses can expose sensitive operational information.

Mitigation: Limit access to authorized users and handle returned data according to the organization's operational data protection requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sandofree/skills/machine-commander-query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The connected MCP service may return tabular or text results inside JSON.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
