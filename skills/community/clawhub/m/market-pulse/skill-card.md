## Description: <br>
Market Pulse provides real-time market analytics for crypto, DeFi, sentiment, stocks, upcoming events, and market overviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lopushok9](https://clawhub.ai/user/lopushok9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and analysts use this skill to request current crypto, DeFi yield, sentiment, stock-index, event, and portfolio-analysis summaries for market research. It helps analyze trades and risks, but transaction execution should happen only through a trusted wallet or broker interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market prices, yields, events, and sentiment can be stale, rate-limited, or inconsistent across public sources. <br>
Mitigation: Ask for fresh sources and timestamps, cross-check conflicting data, and note partial or missing data before relying on the result. <br>
Risk: The skill can analyze trades and portfolio risks, but it is not a trading authority and should not execute transactions. <br>
Mitigation: Use it as a market research helper and execute any trades only through a trusted wallet or broker interface. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lopushok9/market-pulse) <br>
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true) <br>
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng/) <br>
- [DefiLlama yields](https://defillama.com/yields) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown market summaries, ranked lists, and concise analytic guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes timestamps, filters, and data-gap notes when market data freshness matters.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
