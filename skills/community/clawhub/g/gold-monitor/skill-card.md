## Description:

Queries real-time gold prices, the USD index, WTI crude oil prices, the gold/oil ratio, and related investment signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forest-qiao](https://clawhub.ai/user/forest-qiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch current precious-metals, USD index, WTI crude oil, and gold/oil ratio data, then summarize prices and investment signals for market-monitoring conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs Python packages and contacts Sina Finance and AkShare-backed market data sources.

Mitigation: Review dependencies before installation in sensitive environments and allow outbound access only to the disclosed market-data sources.

Risk: The gold/oil ratio output includes investment advice that may be incomplete, stale, or unsuitable for a user's financial situation.

Mitigation: Present the advice as informational market context, include update times, and avoid treating it as personalized financial advice.

Risk: Market-data requests can fail or return incomplete data.

Mitigation: Check for an error field before summarizing results and tell the user when an asset's data could not be fetched.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forest-qiao/skills/gold-monitor)
- [Sina Finance](https://finance.sina.com.cn)
- [Sina Finance quote endpoint pattern](https://hq.sinajs.cn/list={code})

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON from a CLI script, usually summarized by the agent as concise Markdown or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only market-data lookups; outputs include price, change, unit, update time, and an error field when a data fetch fails.]

## Skill Version(s):

2.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
