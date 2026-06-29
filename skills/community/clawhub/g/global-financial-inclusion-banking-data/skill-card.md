## Description: <br>
Global Financial Inclusion & Banking Data lets an agent query bank account ownership, credit access, financial inclusion gender gaps, stock market data, remittances, and related World Bank financial indicators through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to call AgentPMT's financial-sector banking data tool for country and regional analysis of financial inclusion, banking infrastructure, credit, markets, remittances, gender gaps, and SDG-aligned targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on AgentPMT account setup, enabled tools, pricing, and credits before remote calls can succeed. <br>
Mitigation: Confirm the AgentPMT account setup, enabled product access, and current pricing or credit cost before using the skill. <br>
Risk: Prompts or logs could accidentally expose account secrets, wallet private keys, signatures, or payment headers during setup or tool use. <br>
Mitigation: Do not place secrets or payment headers in prompts or logs, and use the referenced setup skills for credential handling. <br>
Risk: Endpoint schemas, examples, and setup details may change after the artifact's 2026-06-24 freshness date. <br>
Mitigation: Reinstall the skill or fetch live schema and instructions before production integration or when details are unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/global-financial-inclusion-banking-data) <br>
- [AgentPMT financial-sector banking marketplace page](https://www.agentpmt.com/marketplace/financial-sector-banking) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>
- [Action schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, JSON, shell commands] <br>
**Output Format:** [Markdown instructions with JSON request and response examples plus shell install commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines one AgentPMT action, query_financial_data, with optional country_or_region, financial_aspect, calculate_gender_gaps, time_period, and include_targets parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
