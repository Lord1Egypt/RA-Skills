## Description: <br>
Queries AgentPMT-hosted digital economy and connectivity data for countries and regions, including internet access, mobile subscriptions, broadband, ICT trade, infrastructure, trends, comparisons, and digital divide analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and policy researchers use this skill to query country or regional digital economy indicators, compare connectivity trends, and assess digital divide or SDG 9.c progress through AgentPMT-hosted remote tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to AgentPMT-hosted services and may consume AgentPMT credits. <br>
Mitigation: Avoid sending confidential investigation context in country or region queries, and confirm account, authorization, and credit expectations before production use. <br>
Risk: The e-government option is limited because World Bank data does not include EGDI directly. <br>
Mitigation: Fetch live schema or instructions before relying on e-government readiness fields, and treat empty or unsupported e-government results as a data limitation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/global-digital-economy-connectivity-data) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/digital-economy-technology) <br>
- [Generated action schema](artifact/schema.md) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, JSON] <br>
**Output Format:** [Markdown instructions with JSON request and response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote AgentPMT calls use the query_digital_data action with country_or_region plus optional digital_aspect, time_period, trend, comparison, and digital-divide parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
