## Description:

Gold Radar helps agents produce gold market briefings, price alerts, weekly outlooks, and gold investment analysis based on market, macroeconomic, and technical signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quiteqiang](https://clawhub.ai/user/quiteqiang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer questions about gold prices, XAU/USD, market trends, price alerts, and gold portfolio decisions. It supports daily briefings, weekly outlooks, technical analysis, and risk-aware trading recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce broad, prescriptive gold-trading guidance that may be mistaken for personalized financial advice.

Mitigation: Treat outputs as informational market analysis, require users to make their own investment decisions, and include risk context with trading recommendations.

Risk: Market data, price levels, and macroeconomic signals can become stale or inaccurate.

Mitigation: Verify current prices and economic events against authoritative sources before relying on any briefing, alert, or trade signal.

Risk: The release carries an unnecessary npm dependency chain, including dependencies resolved through a third-party mirror.

Mitigation: Review dependency metadata and lockfile provenance before installation or deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/quiteqiang/skills/gold-radar)
- [Golden Investment Reference Materials](references/data-sources.md)
- [Golden Investment Strategy Framework](references/investment-strategy.md)
- [Gold Price Key Reference Table](references/price-levels.md)
- [Shanghai Gold Exchange](https://www.sge.com.cn/)
- [LBMA Prices and Data](https://www.lbma.org.uk/prices-and-data)
- [World Gold Council](https://www.gold.org/)
- [Federal Reserve](https://www.federalreserve.gov/)
- [FRED Economic Data](https://fred.stlouisfed.org/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown briefings, alerts, tables, and recommendation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-specific thresholds, watchlists, time zone, currency, holding cost, and risk level when provided.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
