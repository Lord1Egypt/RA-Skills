## Description: <br>
Reads Modbus-TCP PLC telemetry, including holding and input registers, coils, discrete inputs, decode hints, and threshold-based health summaries through the ot-aiops MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and industrial automation engineers use this skill to query authorized Modbus-TCP PLC endpoints, decode register values, read coil states, and summarize health against warn and alarm thresholds. It is intended for read-only telemetry collection and routing, not for PLC writes or broader IT infrastructure diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to query Modbus-TCP endpoints, which may expose operational telemetry if endpoints are not authorized or trusted. <br>
Mitigation: Install only where agents are allowed to query the configured endpoints, and confirm the ot-aiops MCP server and endpoint configuration are trusted before use on production industrial networks. <br>
Risk: Incorrect register addresses, unit IDs, decode settings, or thresholds can produce misleading telemetry or health summaries. <br>
Mitigation: Validate endpoint names, register maps, decode types, and threshold settings against the target PLC documentation before acting on the results. <br>
Risk: The artifact states it was validated with a mocked pymodbus client rather than live PLCs. <br>
Mitigation: Test against representative non-production PLC endpoints before using the skill in operational environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/modbus-tap) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, MCP tool names, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Modbus-TCP queries return decoded register values, bit states, or health summaries through the configured ot-aiops MCP server.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
