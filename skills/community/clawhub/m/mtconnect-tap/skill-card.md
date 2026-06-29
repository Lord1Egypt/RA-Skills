## Description: <br>
Mtconnect Tap helps agents read CNC machine-tool telemetry from MTConnect agents, including device models, current values, bounded samples, assets, and OEE input snapshots through the ot-aiops MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and manufacturing engineers use this skill to inspect MTConnect-enabled CNC machine tools, read current or sampled telemetry, list assets, and collect availability, execution, controller mode, and program values for OEE workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose operational machine telemetry such as programs, execution state, and asset metadata. <br>
Mitigation: Use it only with MTConnect agents you are authorized to access and handle returned telemetry according to site data policies. <br>
Risk: The skill routes requests through an ot-aiops MCP server chosen by the operator. <br>
Mitigation: Confirm the MCP server is trusted before installation or use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/mtconnect-tap) <br>
- [Publisher profile](https://clawhub.ai/user/zw008) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline command examples and JSON-shaped tool outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only MTConnect telemetry queries through the ot-aiops MCP server; bounded samples default to count=100.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
