## Description: <br>
Builds, scaffolds, deploys, and tests Power Automate cloud flows through the FlowStudio MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninihen1](https://clawhub.ai/user/ninihen1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to construct Power Automate flow definitions, wire connector references, deploy new or updated flows, and verify behavior through FlowStudio MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create or modify live Power Automate flows with real automation side effects. <br>
Mitigation: Review the target environment, exact flow ID or creation plan, generated definition or diff, trigger exposure, connector accounts, and callback or SAS-bearing URLs before deployment. <br>
Risk: Testing a deployed flow may send messages, write data, start approvals, or call external APIs. <br>
Mitigation: Use non-production environments when possible and require explicit user confirmation before triggering or resubmitting flow runs. <br>
Risk: The skill depends on sensitive FlowStudio MCP credentials and connector accounts. <br>
Mitigation: Use least-privileged credentials, protect the FLOWSTUDIO_MCP_TOKEN, and confirm connector accounts before executing live operations. <br>


## Reference(s): <br>
- [FlowStudio MCP](https://mcp.flowstudio.app) <br>
- [Flow definition schema](references/flow-schema.md) <br>
- [Trigger type templates](references/trigger-types.md) <br>
- [Core action patterns](references/action-patterns-core.md) <br>
- [Data transform action patterns](references/action-patterns-data.md) <br>
- [Connector action patterns](references/action-patterns-connectors.md) <br>
- [Common build patterns](references/build-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and Python code blocks plus MCP workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FLOWSTUDIO_MCP_TOKEN for live FlowStudio MCP operations.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
