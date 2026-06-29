## Description: <br>
Global Energy Power Grid Data helps agents query AgentPMT-hosted World Bank energy indicators, including electricity access, renewable and fossil energy mix, per-capita consumption, energy intensity, and clean cooking access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and analysts use this skill to call AgentPMT's Global Energy & Power Grid Data tool for country or regional energy access, energy mix, efficiency, and SDG 7 comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AgentPMT MCP or REST use can involve account credentials, payment headers, credits, or wallet-related material. <br>
Mitigation: Review AgentPMT account, payment, and credit usage before connecting access, and keep secrets, wallet keys, mnemonics, signatures, and payment headers out of prompts and logs. <br>
Risk: Energy data availability and recency vary by country, region, and indicator. <br>
Mitigation: Check returned dates, null values, warnings, and live schema details before relying on results for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/global-energy-power-grid-data) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/energy-access-production) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [Action schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON request examples and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides AgentPMT MCP or REST calls that return JSON energy indicator data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
