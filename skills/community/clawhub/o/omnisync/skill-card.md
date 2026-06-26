## Description: <br>
High-performance, standalone synchronization engine for LLM token savings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erkrodcs](https://clawhub.ai/user/erkrodcs) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use OmniSync_Standard to compute local text deltas and cursors for synchronization workflows, reducing repeated content sent between agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted to the sync tool may be returned to the calling agent as delta output. <br>
Mitigation: Only send content that is appropriate for the calling agent to receive, and avoid using the tool as a boundary for sensitive data. <br>
Risk: The MCP gateway may fail to launch because mcp_gateway.py references Any without importing it. <br>
Mitigation: Import Any from typing or otherwise fix the annotation before relying on the gateway in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erkrodcs/omnisync) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON-RPC response containing text with changed status, delta, and cursor] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns SHA-256 cursor values and local text deltas; no external Python dependencies are declared.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and carbonioClaw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
