## Description: <br>
Global Health & Public Health Data lets an agent query life expectancy, mortality, immunization, health expenditure, infectious disease, and demographic health indicators through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to retrieve public-health and demographic indicators for countries or regions, including World Bank-style health data and WHO or SDG benchmark comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are executed through a remote AgentPMT tool and may consume credits. <br>
Mitigation: Use the skill only for public-health or World Bank-style data requests and confirm cost expectations before repeated or automated calls. <br>
Risk: Data availability varies by country and indicator, and the most recent public-health data may lag the current year. <br>
Mitigation: Check returned years and missing values before using results for policy, reporting, or cross-country comparison. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/global-health-public-health-data) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/healthcare-demographics-data) <br>
- [Global Health Public Health Data Schema](artifact/schema.md) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON responses with markdown usage guidance and example request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote AgentPMT queries may cost 10 credits per health data request; responses include resolved country metadata, indicators, optional benchmark comparisons, and demographic context.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
