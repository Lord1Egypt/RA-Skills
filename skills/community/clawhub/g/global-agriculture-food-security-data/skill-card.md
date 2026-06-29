## Description: <br>
Global Agriculture Food Security Data lets agents query AgentPMT-hosted agriculture, food security, malnutrition, land use, and productivity indicators for countries or regions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to call AgentPMT's paid agriculture and food-security data product for country, regional, and global analysis. It supports research on crop yields, undernourishment, malnutrition, land use, productivity, rural context, and SDG 2 indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid remote service use can incur request charges and sends the query inputs to AgentPMT. <br>
Mitigation: Install only when paid agriculture and food-security lookups are intended, invoke the tool explicitly, keep inputs minimal, and avoid sending secrets or unrelated private context. <br>
Risk: Agriculture and food-security results may be delayed or incomplete because source data availability varies by country and indicator. <br>
Mitigation: Review response data notes and source attribution, and confirm freshness before using results for policy, operational, or business decisions. <br>
Risk: Account or payment setup can involve sensitive credentials. <br>
Mitigation: Use the setup guidance for credential handling and do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/global-agriculture-food-security-data) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/agriculture-food-security) <br>
- [Generated action schema](artifact/schema.md) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Analysis, Guidance] <br>
**Output Format:** [JSON responses with structured indicator data, metrics, trends, comparisons, insights, and data notes; Markdown guidance for invocation examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid AgentPMT remote lookups; no local executable runtime is declared. Data may lag current conditions and availability can vary by country and indicator.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
