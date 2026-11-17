## Description:

Global Governance & Institutional Quality Data lets an agent query World Bank WGI governance indicators, including corruption control, rule of law, government effectiveness, political stability, regulatory quality, and voice and accountability through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to fetch and compare governance and institutional quality indicators for countries, regions, income groups, or global aggregates. It supports country risk assessment, anti-corruption analysis, rule of law comparison, political stability monitoring, and investment due diligence workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Governance queries may send country, region, or analysis parameters to AgentPMT and may cost credits.

Mitigation: Keep requests scoped to the minimum needed, confirm account setup before use, and review credit costs before repeated or automated queries.

Risk: Account secrets, wallet keys, signatures, or payment headers could be exposed if included in prompts or logs.

Mitigation: Use the AgentPMT setup skills for credential handling and keep secrets out of prompts, logs, and generated examples.

Risk: Governance indicators are perception-based, may lag by about a year, and can have limited country coverage or trend data.

Mitigation: Treat outputs as decision-support data, check live schema and instructions for production integrations, and verify data availability before relying on trend analysis.

## Reference(s):

- [Global Governance & Institutional Quality Data schema](artifact/schema.md)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/global-governance-institutional-quality-data)
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/governance-institutional-quality)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON request examples and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for AgentPMT MCP or REST calls; tool responses are JSON from the remote AgentPMT product.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
