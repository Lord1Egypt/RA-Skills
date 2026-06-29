## Description: <br>
Cross-protocol, read-only OT troubleshooting via the ot-aiops MCP server for no-data triage, alarm flood analysis, tag health checks, and historian health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, maintenance, and automation engineers use this skill to diagnose blank dashboards, stale or flatline values, alarm floods, bad-actor tags, and OT data-quality issues after read access to industrial telemetry is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Read-only OT diagnostics can expose sensitive operational data through the configured ot-aiops MCP server. <br>
Mitigation: Install and use the skill only with trusted MCP endpoints and restrict access to systems the operator is authorized to inspect. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only diagnostic guidance and expected tool result shapes for an agent using an authorized ot-aiops MCP server.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
