## Description: <br>
Global Population & Demographics Data helps agents query population totals, growth rates, age structure, fertility, migration, and urban-rural demographic indicators through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve and compare World Bank population and demographic indicators for countries or regions, including population size, growth, age structure, fertility, migration, and urban-rural splits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AgentPMT account credentials or payment headers could be exposed if copied into prompts or logs. <br>
Mitigation: Keep credentials and payment headers out of prompts and logs, and use the referenced AgentPMT setup skill for credential handling. <br>
Risk: Use depends on AgentPMT hosted service access, account setup, and credit cost. <br>
Mitigation: Confirm the intended AgentPMT service, account route, enabled tool, and credit cost before installation or production use. <br>
Risk: Population and demographic data may lag the current year or be unavailable for some countries, regions, or indicators. <br>
Mitigation: Check the returned time period, warnings, and live schema before relying on results for current-year analysis. <br>


## Reference(s): <br>
- [Global Population & Demographics Data Schema](artifact/schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/global-population-demographics-data) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/population-demographics) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown instructions with JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote responses are JSON returned by AgentPMT-hosted tool calls; no local command runtime is declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
