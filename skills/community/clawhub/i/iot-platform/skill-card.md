## Description: <br>
Guide to connect Cloud Studio IoT's OpenClaw platform to MCP clients for gateway access, IoT device commands, sensor reads, and channel management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sobdev](https://clawhub.ai/user/Sobdev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure MCP client connections to an OpenClaw gateway, verify gateway health, and troubleshoot local or Tailscale-based access to IoT devices, sensors, channels, and gateway agent tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes exposing a powerful OpenClaw MCP control endpoint for device, channel, and agent-control functions, including public remote access patterns. <br>
Mitigation: Prefer loopback or tailnet-only Tailscale Serve access; avoid Tailscale Funnel unless strong access controls, restricted tools, a strong unique secret, and monitoring are in place. <br>


## Reference(s): <br>
- [OpenClaw Gateway Documentation](https://docs.openclaw.ai/gateway) <br>
- [Cloud Studio IoT](https://cloudstudioiot.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for configuring MCP clients and OpenClaw gateway access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
