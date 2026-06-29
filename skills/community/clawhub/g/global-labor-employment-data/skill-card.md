## Description: <br>
Global Labor Employment Data lets agents query AgentPMT-hosted World Bank labor market indicators, including labor force participation, unemployment, sector employment, gender gaps, and youth employment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide AgentPMT remote calls for country, regional, and global labor-market research, including workforce participation, unemployment, sector composition, gender gaps, youth employment, and SDG 8 monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AgentPMT queries are remote calls and may spend credits when invoked. <br>
Mitigation: Use the skill only when AgentPMT labor-market data is intended, confirm the enabled account route, and review the 5-credit query cost before use. <br>
Risk: Account credentials or payment details could be exposed if copied into prompts or logs. <br>
Mitigation: Use the setup skill for credential handling and keep API credentials, payment headers, wallet secrets, and similar sensitive values out of prompts and logs. <br>
Risk: Endpoint schemas, setup details, or examples may drift after the documented freshness window. <br>
Mitigation: Refresh the skill or fetch the live AgentPMT schema before production integrations or when relying on it more than seven days after the listed update date. <br>
Risk: Labor-market data availability varies by country and recent values can lag current conditions. <br>
Mitigation: Check returned source years and warnings, and qualify analysis when indicators are missing, sparse, or delayed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/global-labor-employment-data) <br>
- [AgentPMT Labor Market Employment Marketplace Page](https://www.agentpmt.com/marketplace/labor-market-employment) <br>
- [Action Schema](schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, JSON] <br>
**Output Format:** [Markdown instructions with JSON request examples and expected JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote AgentPMT calls may require account setup and can spend 5 credits per query.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
