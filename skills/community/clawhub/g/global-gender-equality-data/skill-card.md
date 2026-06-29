## Description: <br>
Global Gender Equality Data helps agents query gender equality indicators for any country or region through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to query country or regional gender equality indicators, compare gaps across labor, education, political, legal, health, economic, and violence dimensions, and support SDG 5 analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote tool calls may receive country, region, and analysis parameters that are broader than needed. <br>
Mitigation: Keep inputs scoped to the minimum needed for the gender equality query and avoid sending secrets or unrelated workspace data. <br>
Risk: Underlying World Bank and Women, Business and the Law indicators can lag current conditions or be unavailable for some countries. <br>
Mitigation: Check data recency and availability before using outputs for policy, business, or public reporting decisions. <br>
Risk: Account credentials or payment-related material could be exposed if copied into prompts or logs during setup. <br>
Mitigation: Use the referenced AgentPMT setup guidance for credential handling and do not place secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs. <br>


## Reference(s): <br>
- [Generated action schema](artifact/schema.md) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/gender-equality-women-s-empowerment) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/global-gender-equality-data) <br>
- [AgentPMT account MCP and REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON] <br>
**Output Format:** [Markdown instructions with JSON request and response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines one remote action, query_gender_data, with country_or_region required and optional gender_aspect, calculate_gaps, and time_period parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
