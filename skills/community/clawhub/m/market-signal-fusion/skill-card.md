## Description:

Adaptive-language stock-analysis skill that interprets macro and political news, fuses it with retail/social sentiment, applies quantified value fallback rules, and outputs machine-readable stock ideas with valuation and technical plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yellowzijian](https://clawhub.ai/user/yellowzijian)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to produce structured stock-market analysis that combines macro catalysts, retail sentiment, valuation fallback screening, confidence gates, and technical trade planning. It is intended for agent workflows that need both human-readable finance commentary and machine-readable JSON outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market outputs may be mistaken for personalized financial advice.

Mitigation: Treat outputs as market analysis only and independently verify prices, metrics, catalysts, and suitability before acting.

Risk: Configured web, market-data, or social-data tools may send tickers and related context to external services.

Mitigation: Review connected tool providers and avoid submitting sensitive account, portfolio, or personal information unless the deployment permits it.

Risk: Incomplete or stale market, sentiment, valuation, or technical data can reduce decision quality.

Mitigation: Use the skill's confidence gates, reason codes, and unavailable-data disclosures to downgrade conviction or skip unsupported picks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yellowzijian/skills/market-signal-fusion)
- [Publisher profile](https://clawhub.ai/user/yellowzijian)
- [ClawHub homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Human-readable Markdown report plus an optional strict JSON block for downstream processing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapts output language to the user's prompt and preserves stable English keys for structured JSON.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
