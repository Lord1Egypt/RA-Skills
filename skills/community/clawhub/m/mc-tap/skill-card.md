## Description: <br>
Read Mitsubishi MELSEC PLC telemetry over the MC protocol, including CPU status, word and bit devices, scattered reads, and an off-by-default governed word-write path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OT engineers and automation developers use this skill to route Mitsubishi MELSEC PLC telemetry tasks to ot-aiops MCP tools for read-first diagnostics, CPU status checks, and controlled word writes when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Word write operations can affect production control systems. <br>
Mitigation: Keep dry-run enabled unless authorized, verify the endpoint and device range, and require the stated approval and confirmation process before applying writes. <br>
Risk: The skill describes preview validation against a mocked client rather than live PLCs. <br>
Mitigation: Validate against non-production PLCs and confirm the target plctype and 3E frame compatibility before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/mc-tap) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline command examples and JSON-shaped tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-first MC protocol routing; write operations default to dry-run and require approval before applying changes.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
