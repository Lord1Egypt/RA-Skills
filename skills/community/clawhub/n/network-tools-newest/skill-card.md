## Description:

Network Tools provides AgentPMT-hosted network utilities for IP conversion and validation, subnet and CIDR calculations, MAC formatting, port lookup, DNS resolution, private IP detection, and related network analysis tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, network administrators, security analysts, and infrastructure engineers use this skill to perform network calculations, address conversions, DNS lookups, port classification, and IP range checks through AgentPMT-hosted tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network inputs such as internal hostnames, private CIDRs, MAC addresses, customer IPs, or topology details may be sent to a third-party service.

Mitigation: Use only the minimum input needed, avoid sensitive internal topology unless sharing with AgentPMT is intended, and review enterprise or incident-response use before installation.

Risk: The skill references setup-install commands that may be unpinned.

Mitigation: Prefer pinned and verified setup paths, and review installation sources before deploying the skill.

Risk: Actions consume AgentPMT account credits.

Mitigation: Confirm expected cost and account authorization before running repeated lookups or automation.

## Reference(s):

- [Network Tools marketplace page](https://www.agentpmt.com/marketplace/network-tools)
- [Network Tools ClawHub page](https://clawhub.ai/agentpmt/skills/network-tools-newest)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines 15 AgentPMT network utility actions; most actions take string parameters and return JSON results from remote tool calls.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
