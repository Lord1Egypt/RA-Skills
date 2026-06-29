## Description: <br>
Global Governance & Institutional Quality Data helps agents query country and regional governance indicators, including corruption control, rule of law, government effectiveness, political stability, regulatory quality, and voice and accountability through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch World Bank Worldwide Governance Indicators for country risk analysis, institutional quality research, regional comparison, and governance trend monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Governance indicators are perception-based and may lag current conditions. <br>
Mitigation: Treat results as decision-support data, check the reported time period, and corroborate material conclusions with current local or primary sources. <br>
Risk: Remote tool usage may depend on live AgentPMT schemas, account permissions, and scoped credentials. <br>
Mitigation: Fetch live schema before production integration, verify the target tool, and keep API credentials scoped and revocable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/global-governance-institutional-quality-data) <br>
- [AgentPMT Marketplace Listing](https://www.agentpmt.com/marketplace/governance-institutional-quality) <br>
- [Publisher Profile](https://clawhub.ai/user/agentpmt) <br>
- [Action Schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with JSON request examples; remote tool responses return structured governance data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries may include governance aspect, time period, percentile ranks, historical trends, and peer comparison options.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
