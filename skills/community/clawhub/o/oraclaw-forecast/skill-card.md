## Description:

Time series forecasting for AI agents using ARIMA and Holt-Winters predictions with confidence intervals for revenue, traffic, prices, or other sequential data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to forecast future values from numeric time-series data, compare ARIMA and Holt-Winters approaches, and receive confidence intervals for planning decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forecast requests require an OraClaw API key and may send business-sensitive numeric time-series data to the OraClaw service.

Mitigation: Confirm the data is appropriate to share with the service and protect ORACLAW_API_KEY as a credential before use.

Risk: Forecast calls are paid at the listed USDC/x402 price after any applicable free tier.

Mitigation: Review expected usage volume and pricing before enabling automated or repeated calls.

Risk: Long-horizon forecasts and confidence intervals may become less reliable as the requested forecast steps increase.

Mitigation: Prefer short forecast horizons, review confidence intervals, and treat outputs as decision support rather than guarantees.

## Reference(s):

- [OraClaw Forecast](https://oraclaw.dev/forecast)
- [ClawHub Skill Page](https://clawhub.ai/whatsonyourmind/skills/oraclaw-forecast)
- [Publisher Profile](https://clawhub.ai/user/whatsonyourmind)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Markdown or structured text describing forecast values, confidence intervals, method choice, and required API-key configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecast calls require ORACLAW_API_KEY and may send numeric time-series data to the OraClaw service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
