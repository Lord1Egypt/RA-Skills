## Description: <br>
Oraclaw Forecast predicts future values from historical time series using ARIMA and Holt-Winters models with confidence intervals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to forecast revenue, traffic, prices, demand, or other sequential data and receive forecast values with confidence intervals. It supports non-seasonal ARIMA forecasts and seasonal Holt-Winters forecasts when a season length is supplied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected time-series values to a third-party forecasting provider and requires an OraClaw API key. <br>
Mitigation: Avoid submitting confidential revenue, customer, trading, or other sensitive data unless the provider's privacy, billing, and security terms are acceptable. <br>
Risk: Forecast confidence intervals widen over longer horizons, and long-range predictions may be misleading. <br>
Mitigation: Use short forecast horizons, review confidence bounds, and validate outputs against domain knowledge before using them for business decisions. <br>
Risk: The skill has disclosed per-forecast pricing and payment requirements. <br>
Mitigation: Confirm billing expectations, free-tier limits, and API key scope before high-volume use. <br>


## Reference(s): <br>
- [OraClaw Forecast homepage](https://oraclaw.dev/forecast) <br>
- [ClawHub skill page](https://clawhub.ai/whatsonyourmind/oraclaw-forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, structured data, guidance] <br>
**Output Format:** [Forecast values with lower and upper 95% confidence bounds, typically returned as structured text or JSON-like data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ORACLAW_API_KEY. Inputs include historical data, forecast steps, method, and optional seasonLength for Holt-Winters. The release states $0.05 per forecast with a free tier.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
