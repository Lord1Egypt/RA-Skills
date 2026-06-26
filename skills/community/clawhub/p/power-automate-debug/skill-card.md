## Description: <br>
Debug failing Power Automate cloud flows using the FlowStudio MCP server by inspecting action-level inputs and outputs to identify root causes hidden by top-level status codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninihen1](https://clawhub.ai/user/ninihen1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to investigate failed Power Automate cloud flow runs, inspect runtime action inputs and outputs, trace expression, connector, and HTTP failures, and verify proposed fixes through FlowStudio MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to update and rerun live Power Automate flows, which may affect production automations. <br>
Mitigation: Require explicit approval after the agent shows the target flow, proposed change, expected downstream effects, rollback plan, and test-environment verification plan. <br>
Risk: The skill requires a FlowStudio MCP token and access to sensitive automation data. <br>
Mitigation: Use a least-privilege token, provide it only through the configured environment variable, and install the skill only when the FlowStudio MCP server is trusted. <br>
Risk: Power Automate action outputs can include large or sensitive payloads while debugging. <br>
Mitigation: Inspect only the fields needed for diagnosis, limit printed output, and avoid retaining credentials, personal data, or unrelated payload contents in agent responses. <br>


## Reference(s): <br>
- [FlowStudio MCP](https://mcp.flowstudio.app) <br>
- [FlowStudio MCP - Common Power Automate Errors](references/common-errors.md) <br>
- [FlowStudio MCP - Debug Workflow](references/debug-workflow.md) <br>
- [Expression error in child flow](https://github.com/ninihen1/power-automate-mcp-skills/blob/main/examples/fix-expression-error.md) <br>
- [Data entry, not a flow bug](https://github.com/ninihen1/power-automate-mcp-skills/blob/main/examples/data-not-flow.md) <br>
- [Null value crashes child flow](https://github.com/ninihen1/power-automate-mcp-skills/blob/main/examples/null-child-flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API calls, Configuration] <br>
**Output Format:** [Markdown with Python code blocks and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FlowStudio MCP access and FLOWSTUDIO_MCP_TOKEN; agents should confirm current tool names and schemas with tools/list before making calls.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
