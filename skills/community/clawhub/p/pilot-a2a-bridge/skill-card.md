## Description: <br>
Bridge A2A (Agent-to-Agent) protocol messages over Pilot tunnels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to bridge Agent-to-Agent messages through Pilot's encrypted overlay network when agents need reliable cross-network communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incoming A2A messages may be untrusted or malformed. <br>
Mitigation: Validate sender identity, message type, payload schema, and size before allowing an agent to act on a message. <br>
Risk: Networked messaging can expose sensitive data to remote agents or deployments. <br>
Mitigation: Use the skill only with trusted pilotctl and Pilot daemon deployments, and avoid sending secrets unless approved by the deployment policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-a2a-bridge) <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot daemon, and A2A-compatible agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
