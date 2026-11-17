## Description:

Global Agriculture & Food Security Data lets agents query agricultural production, food security, malnutrition, land use, productivity, rural context, trends, and regional comparisons through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to retrieve World Bank and FAO agriculture and food-security indicators by country, region, income group, or global aggregate. It supports food security monitoring, crop-yield trend analysis, productivity gap review, land-use comparison, and SDG 2 research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents toward paid AgentPMT requests.

Mitigation: Use it only when paid agriculture and food-security data queries are intended, and review request parameters before execution.

Risk: Referenced setup skills handle account connection and credential paths.

Mitigation: Review and pin setup skill installation paths before use, and keep secrets, wallet material, and payment headers out of prompts and logs.

## Reference(s):

- [AgentPMT marketplace: Agriculture Food Security](https://www.agentpmt.com/marketplace/agriculture-food-security)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/global-agriculture-food-security-data)
- [AgentPMT publisher profile](https://clawhub.ai/user/agentpmt)
- [Schema reference](artifact/schema.md)

## Skill Output:

**Output Type(s):** [guidance, API Calls, Configuration instructions, JSON]

**Output Format:** [Markdown instructions with JSON call examples and JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include indicator data, productivity metrics, rural context, trends, regional comparisons, insights, SDG alignment, and data notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
