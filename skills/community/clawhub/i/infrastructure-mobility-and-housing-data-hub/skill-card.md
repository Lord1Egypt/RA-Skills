## Description: <br>
Infrastructure, Mobility, and Housing Data Hub helps agents query World Bank infrastructure, mobility, housing, urban development, and access-gap data by country or region through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to retrieve country or regional infrastructure indicators, access gaps, SDG progress, and urban-rural breakdowns for planning, benchmarking, and reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends country, regional, and planning context to an AgentPMT-hosted remote tool. <br>
Mitigation: Confirm that the information is appropriate to send to AgentPMT before invocation and keep inputs scoped to the minimum needed for the task. <br>
Risk: The remote action is described as a paid AgentPMT/x402 route. <br>
Mitigation: Use the referenced setup skills for credential, wallet, and payment handling, and confirm cost-bearing calls before execution. <br>
Risk: World Bank data availability varies by country, indicator, and time period. <br>
Mitigation: Review returned warnings, years, and missing-data fields before using results in decisions or reports. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/infrastructure-mobility-and-housing-data-hub) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/infrastructure-urban-development) <br>
- [Action Schema](artifact/schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [No-account AgentAddress/x402 Setup](https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, JSON] <br>
**Output Format:** [Markdown instructions with JSON tool-call examples and schema references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to call a paid AgentPMT-hosted World Bank infrastructure data lookup action and to treat returned JSON as the source of truth.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
