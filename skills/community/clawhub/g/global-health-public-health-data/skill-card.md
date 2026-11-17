## Description:

Global Health & Public Health Data: Query life expectancy, mortality rates, immunization coverage, health expenditure, infectious disease. Use when an agent needs global health & public health data, healthcare demographics data, research life expectancy by country, compare infant and child mortality rates across regions, track immunization coverage trends, analyze health expenditure as percentage of gdp, query health data, country or region through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to query AgentPMT-hosted global health data for country and regional public health analysis, including life expectancy, mortality, immunization, expenditure, infectious disease, and demographic indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional setup instructions include unpinned npx commands.

Mitigation: Prefer the OpenClaw install path, or verify the skills.sh package and AgentPMT skill source before using the npx setup commands.

Risk: Live calls may involve AgentPMT account credentials, payment headers, or credits.

Mitigation: Use the setup skill for credential handling, keep secrets out of prompts and logs, and submit only the minimum query inputs needed.

Risk: Returned public health data can have country, indicator, and freshness gaps.

Mitigation: Check returned years, units, warnings, and schema guidance before using results for policy, research, or comparative conclusions.

## Reference(s):

- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/healthcare-demographics-data)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/global-health-public-health-data)
- [Action schema](artifact/schema.md)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, JSON]

**Output Format:** [Markdown instructions with JSON request and response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote AgentPMT calls return JSON health indicators and may require AgentPMT account setup and credits.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
