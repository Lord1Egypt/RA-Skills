## Description: <br>
Risk assessment engine for AI agents that calculates VaR, CVaR, stress tests, and multi-factor risk scores using Monte Carlo simulation for trading agents, lending agents, and portfolio managers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, trading agents, lending agents, and portfolio managers use this skill to estimate downside exposure, stress scenarios, credit risk, and agreement among risk indicators before making financial decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a paid external risk-assessment service and requires an API key. <br>
Mitigation: Use a scoped API key where possible, monitor billing or spending limits, and install only when the paid OraClaw service is intended. <br>
Risk: Portfolio or credit inputs may contain confidential financial data. <br>
Mitigation: Avoid sending confidential portfolio, trading, or credit data unless the provider's data handling is acceptable for the use case. <br>
Risk: Financial risk estimates can be misleading if assumptions, distributions, or scenario inputs are wrong. <br>
Mitigation: Treat outputs as decision support, review model assumptions, and report both VaR and CVaR with stress scenarios instead of relying on VaR alone. <br>


## Reference(s): <br>
- [OraClaw Risk homepage](https://oraclaw.dev/risk) <br>
- [ClawHub listing](https://clawhub.ai/whatsonyourmind/oraclaw-risk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Analysis, Guidance, API Calls] <br>
**Output Format:** [Markdown text with structured financial risk metrics and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ORACLAW_API_KEY; paid usage is priced in USDC according to the skill metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
