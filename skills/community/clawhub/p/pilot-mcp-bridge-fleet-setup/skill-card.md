## Description: <br>
Deploy an MCP and A2A bridge fleet with three agents: an MCP gateway, an A2A bridge, and a tool registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure a three-node Pilot bridge fleet that connects MCP servers, A2A agents, and a central tool registry over Pilot tunnels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the listed ClawHub skills and running Pilot handshakes can add skills, create trust relationships, and persist Pilot configuration under the user's home directory. <br>
Mitigation: Review the skill installs and pilotctl handshakes before execution, and run them only on machines intended to join the described bridge fleet. <br>
Risk: The bridge fleet routes MCP tool calls and A2A tasks through trusted Pilot peers, so incorrect peer selection can expose workflow traffic to an unintended node. <br>
Mitigation: Use a unique deployment prefix, handshake only expected peers, and verify the resulting trust relationships with pilotctl trust. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-mcp-bridge-fleet-setup) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes role-specific setup steps, hostname conventions, trust handshakes, and manifest examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
