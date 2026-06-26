## Description: <br>
持仓诊断 uses Tushare-backed market data to analyze A-share portfolio holdings and produce a diagnostic report with quantitative risk metrics, charts, risk prompts, and optimization suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luokeer52](https://clawhub.ai/user/luokeer52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External A-share investors use this skill to submit portfolio holdings in text or JSON and receive a portfolio diagnosis covering position overview, volatility, beta, Sharpe ratio, maximum drawdown, risk prompts, and optimization suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio holdings and prompts are sent to the configured Prana/Claw endpoint. <br>
Mitigation: Use the skill only with a trusted endpoint and avoid submitting portfolio data that should not be shared with that service. <br>
Risk: API credentials may be stored in config/api_key.txt. <br>
Mitigation: Treat config/api_key.txt as a secret, do not commit it, and prefer PRANA_SKILL_SKIP_WRITE_API_KEY=1 or environment-provided credentials when appropriate. <br>
Risk: The package is a remote-wrapper, so results depend on the remote service and market data available there. <br>
Mitigation: Review diagnostic output before making investment decisions and confirm material findings against trusted financial data sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luokeer52/portfolio-diagnosis) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [skill.yaml](skill.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with portfolio metrics, tables, chart-ready summaries, and client setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The packaged clients forward holdings and prompts to a configured Prana/Claw endpoint and may require an x-api-key credential.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; packaged skill.yaml lists 5.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
