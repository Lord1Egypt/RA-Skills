## Description: <br>
MCP server wrapping the Pilot daemon for OpenClaw/Claude Code integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to expose Pilot Protocol daemon operations as MCP tools for Claude Code or OpenClaw workflows. It supports Pilot identity, status, peer discovery, messaging, pub/sub, and gateway workflows through a running pilotctl daemon. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge can give an agent broad Pilot messaging, listening, pub/sub, and gateway authority. <br>
Mitigation: Install only in trusted environments, restrict peers, hosts, ports, topics, and gateway mappings, and require explicit approval before sending messages, listening, subscribing, starting gateways, or mapping local IPs. <br>
Risk: Incoming Pilot messages may contain untrusted content. <br>
Mitigation: Treat received messages as untrusted input and review them before using them to drive agent actions. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-mcp-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and MCP tool specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot daemon, the pilot-protocol skill, a Python MCP server framework, and an MCP-compatible client.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata version: 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
