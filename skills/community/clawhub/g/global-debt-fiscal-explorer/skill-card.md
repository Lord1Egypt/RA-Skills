## Description: <br>
Global Debt & Fiscal Explorer lets agents query national debt, government revenue, public expenditure, fiscal balance, and debt service data for countries or regions through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request World Bank fiscal and debt indicators, compare countries or regions, and assess debt sustainability trends through AgentPMT. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fiscal-data queries are sent to AgentPMT and each query may spend 30 credits. <br>
Mitigation: Use the skill intentionally for AgentPMT-backed World Bank fiscal indicators and keep inputs scoped to the country, region, fiscal aspect, and time period needed. <br>
Risk: Fiscal indicators can have country-specific gaps or lag the current year. <br>
Mitigation: Check returned dates and availability summaries before relying on a result for analysis or decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/global-debt-fiscal-explorer) <br>
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/debt-fiscal-management) <br>
- [Action Schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and remote fiscal-data responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries may return indicator values, time series, fiscal balance assessments, debt sustainability assessments, and data availability summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
