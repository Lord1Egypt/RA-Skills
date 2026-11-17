## Description:

Financial event impact analyzer that fetches breaking news, tracks metals, oil, crypto, and stock prices, and predicts short-, medium-, and long-term market ripple effects with three-layer impact analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stn0000](https://clawhub.ai/user/stn0000)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to collect public market news and price data, then generate structured financial event impact analysis across immediate, 1-12 hour, and 12-24 hour horizons. The skill is for informational and educational analysis and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch live public data and user-provided URLs, so private, local, internal, or authenticated URLs could expose sensitive content.

Mitigation: Grant network access only when needed, prefer explicit event text or public HTTPS news links, and avoid private or authenticated URLs.

Risk: Financial event predictions can be incorrect or misread as trading recommendations.

Mitigation: Keep the informational disclaimer, present predictions as uncertain, include contrarian risk, and do not provide specific buy or sell instructions.

Risk: Dependency installation uses Python package installation for yfinance.

Mitigation: Install dependencies in an isolated virtual environment and pin dependency versions before operational use.

## Reference(s):

- [Market Oracle ClawHub skill page](https://clawhub.ai/stn0000/skills/market-oracle)
- [Market Oracle project homepage](https://github.com/stn0000/market-oracle)
- [Google News RSS search endpoint](https://news.google.com/rss/search)
- [Yahoo Finance RSS endpoint](https://feeds.finance.yahoo.com/rss/2.0/headline)
- [Finviz news RSS endpoint](https://finviz.com/news_export.ashx?v=3)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis, Guidance, Shell commands]

**Output Format:** [Markdown-style text report or JSON context containing event details, market data, news context, global headlines, and predictions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include informational risk disclaimers and may depend on live public network data from news feeds and yfinance.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
