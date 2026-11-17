## Description:

Queries global financial inclusion and banking indicators, including account ownership, credit access, gender gaps, stock market data, remittances, and mobile money adoption through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and policy researchers use this skill to query country, regional, and global banking and financial inclusion data. It supports comparisons across regions, gender gap analysis, credit and lending research, remittance analysis, stock market indicators, and SDG-aligned financial access tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries are sent to a paid remote AgentPMT service.

Mitigation: Send only the minimum query data needed, keep credentials out of prompts and logs, and review account or payment setup before use.

Risk: Setup skills or install sources can affect credential handling and runtime behavior.

Mitigation: Use pinned or reviewed install sources for related setup skills and follow the AgentPMT account MCP/REST setup guidance.

Risk: Endpoint schemas, examples, or product availability may change after publication.

Mitigation: Refresh the skill or fetch live schema and instructions before new production integrations or when parameters and outputs are unclear.

## Reference(s):

- [AgentPMT Financial Sector Banking Marketplace Page](https://www.agentpmt.com/marketplace/financial-sector-banking)
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/global-financial-inclusion-banking-data)
- [Generated Action Schema](artifact/schema.md)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON, Configuration instructions]

**Output Format:** [Markdown guidance with JSON request and response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote AgentPMT calls return financial indicator data, availability summaries, comparisons, and optional target or SDG alignment details.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
