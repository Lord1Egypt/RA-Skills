## Description: <br>
Pro+ subscription required; tenant-wide Power Automate flow health monitoring, failure-rate analytics, and asset inventory using the FlowStudio MCP cached store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninihen1](https://clawhub.ai/user/ninihen1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Tenant administrators and Power Platform operators use this skill to monitor tenant-wide Power Automate health, review failure trends, audit makers, and inventory flows, environments, connections, and Power Apps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive tenant-wide Power Platform data, including cached flow definitions, trigger URLs, maker details, and run history. <br>
Mitigation: Use it only with trusted tenant administrators, prefer aggregate reports, and avoid sharing raw trigger URLs or full flow definitions unless explicitly needed. <br>
Risk: The skill can guide changes to monitoring, notification, tagging, criticality, and governance metadata. <br>
Mitigation: Require clear user approval before any update and confirm the intended flow, environment, and governance fields before applying changes. <br>
Risk: Store data may be stale because FlowStudio scans Power Automate data on a schedule. <br>
Mitigation: Check scanned and nextScan fields before relying on cached results, and use live diagnostic tools when fresh run-level evidence is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ninihen1/power-automate-monitoring) <br>
- [FlowStudio MCP](https://mcp.flowstudio.app) <br>
- [FlowStudio Teams monitoring guide](https://learn.flowstudio.app/teams-monitoring) <br>
- [FlowStudio pricing](https://mcp.flowstudio.app/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool names, workflow steps, filters, and response-shape notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include aggregate monitoring summaries, inventory tables, governance recommendations, and requested tool calls.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
