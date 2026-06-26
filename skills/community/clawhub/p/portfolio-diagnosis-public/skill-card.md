## Description: <br>
Provides A-share portfolio diagnosis for investors by using Tushare-driven market and historical data to assess volatility, beta, Sharpe ratio, maximum drawdown, position mix, risks, and optimization suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[super-max21](https://clawhub.ai/user/super-max21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External A-share investors and agents assisting them use the skill to turn holdings inputs into quantitative portfolio risk diagnostics, risk warnings, and optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio holdings, cost basis, positions, and related prompts are sent to the configured Prana service. <br>
Mitigation: Install only when that data sharing is acceptable for the user's privacy and compliance context; redact sensitive holdings when needed. <br>
Risk: Prana API credentials may be stored in config/api_key files. <br>
Mitigation: Use a dedicated or revocable API key and keep config/api_key files out of public repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/super-max21/portfolio-diagnosis-public) <br>
- [Publisher profile](https://clawhub.ai/user/super-max21) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or text portfolio diagnosis report with quantitative risk metrics and chart-oriented analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Prana credentials; portfolio prompts are sent to the configured Prana service.] <br>

## Skill Version(s): <br>
5.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
