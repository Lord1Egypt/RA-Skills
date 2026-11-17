## Description:

Provides real-time market analytics for crypto, DeFi yields, sentiment, upcoming crypto events, and traditional market overviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lopushok9](https://clawhub.ai/user/lopushok9)

### License/Terms of Use:


## Use Case:

External users and market analysts use this skill to request concise market intelligence, portfolio context, DeFi yield summaries, risk notes, and current market overviews from public web and API sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live market data and portfolio recommendations can be incomplete, stale, or unsuitable for a user's financial situation.

Mitigation: Treat outputs as informational, show timestamps and data gaps, cross-check conflicting sources, and make financial decisions through qualified review.

Risk: Users may share wallet seed phrases, exchange credentials, or private account exports while asking for portfolio analysis.

Mitigation: Do not request or process secrets; users should keep credentials private and execute trades only through their own trusted wallet or brokerage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lopushok9/skills/market-pulse)
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true)
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with concise market summaries, ranked lists, comparisons, timestamps, and cited metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public web and API lookups for current market data; does not execute trades or handle transactions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
