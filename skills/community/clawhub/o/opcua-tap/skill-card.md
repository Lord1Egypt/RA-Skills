## Description: <br>
Reads OPC-UA servers over opc.tcp by browsing nodes, reading values, sampling bounded telemetry, surfacing alarms, and summarizing health through the external ot-aiops MCP server. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and industrial engineers use this skill to inspect authorized OPC-UA servers, browse node trees, read telemetry values, sample bounded data, review historical values, and surface alarms or health anomalies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connecting to unauthorized OPC-UA endpoints can expose industrial telemetry or operational details. <br>
Mitigation: Use the skill only with OPC-UA endpoints you are authorized to inspect and verify the external ot-aiops MCP server and encrypted credential store before connecting. <br>
Risk: The skill is preview-status and does not validate OPC-UA Sign/Encrypt message security for real industrial deployments. <br>
Mitigation: Avoid production or safety-critical use until the endpoint, credential handling, and required message security posture are independently validated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/opcua-tap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands and JSON-like OPC-UA telemetry summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only OPC-UA access routed through the external ot-aiops MCP server; sampling and history queries are bounded.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
