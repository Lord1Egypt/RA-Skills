## Description: <br>
Network Tools provides AgentPMT-hosted utilities for IPv4 conversion, subnet and CIDR calculations, MAC address formatting, port validation, DNS lookups, reverse DNS, IP classification, and IPv6 generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, network administrators, and security analysts use this skill to call AgentPMT-hosted network utilities for subnet planning, IP conversion, DNS resolution, and address classification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote network-utility calls may send hostnames, IP addresses, or investigative targets to AgentPMT. <br>
Mitigation: Avoid submitting private customer hostnames, internal domains, private IP ranges, MAC addresses, or investigative targets unless external processing by AgentPMT is approved. <br>
Risk: Account, wallet, or payment credentials may be exposed if placed in prompts or logs. <br>
Mitigation: Handle account, wallet, and payment credentials only through the referenced setup flow, not in prompts or logs. <br>


## Reference(s): <br>
- [Network Tools schema](./schema.md) <br>
- [Network Tools marketplace page](https://www.agentpmt.com/marketplace/network-tools) <br>
- [Network Tools ClawHub page](https://clawhub.ai/agentpmt/network-tools-newest) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, JSON] <br>
**Output Format:** [Markdown instructions with JSON request and response patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote AgentPMT calls; input values are strings unless an action declares no input.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
