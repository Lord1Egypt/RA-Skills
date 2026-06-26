## Description: <br>
Manage a Tailscale tailnet from chat by checking status, listing devices, pinging hosts, running diagnostics, and checking serve/funnel configuration with public IP masking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lookupmark](https://clawhub.ai/user/lookupmark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Tailscale tailnet state, devices, connectivity, diagnostics, serve status, and whois results from an agent chat session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal tailnet device, identity, and network diagnostic details to the agent session. <br>
Mitigation: Use it only in trusted sessions where showing tailnet status, devices, diagnostics, serve status, and whois results is acceptable. <br>
Risk: Public IP masking is a display safeguard, not a hard privacy boundary. <br>
Mitigation: Review output before sharing it and avoid relying on masking as the only control for sensitive network details. <br>
Risk: The skill runs the local tailscale CLI. <br>
Mitigation: Install it only on systems where the agent is allowed to execute read-only Tailscale status and diagnostic commands. <br>


## Reference(s): <br>
- [Tailscale CLI documentation](https://tailscale.com/kb/1080/cli) <br>
- [ClawHub skill page](https://clawhub.ai/lookupmark/lookupmark-tailscale-manager) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lookupmark) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Public IPs are masked in displayed output; Tailscale private IPs, DNS names, and online status may be shown.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
