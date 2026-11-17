## Description:

Tenant-wide Power Automate flow health monitoring, failure rate analytics, and asset inventory using the FlowStudio MCP cached store for Pro+ subscribers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninihen1](https://clawhub.ai/user/ninihen1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform administrators, and governance teams use this skill to analyze tenant-wide Power Automate health, failure trends, maker activity, asset inventory, and compliance posture from FlowStudio cached store data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tenant-wide FlowStudio cached-store access can expose sensitive flow, owner, connection, trigger URL, and governance metadata.

Mitigation: Install only where FLOWSTUDIO_MCP_TOKEN access is appropriate for tenant-wide monitoring, and avoid sharing trigger URLs or tenant data in chats, tickets, or logs.

Risk: The skill can guide persistent governance changes through update_store_flow, including monitoring, notification, criticality, ownership, tier, and security metadata.

Mitigation: Require explicit user intent before suggesting or executing metadata updates, and review the proposed field changes before applying them.

Risk: FlowStudio cached-store data may be stale because scans run periodically.

Mitigation: Check scanned or nextScan freshness fields before treating cached health metrics as current operational truth.

## Reference(s):

- [Power Automate Monitoring ClawHub release](https://clawhub.ai/ninihen1/skills/power-automate-monitoring)
- [FlowStudio MCP homepage](https://mcp.flowstudio.app)
- [FlowStudio Teams monitoring documentation](https://learn.flowstudio.app/teams-monitoring)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool names, JSON response-shape examples, and workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FLOWSTUDIO_MCP_TOKEN and FlowStudio Pro+ access; may guide tenant health summaries, cached-store queries, and governance metadata updates.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
