## Description: <br>
Free meme coin signal scanner. Aggregates DEXScreener, Pump.fun, GeckoTerminal, CoinGecko trending data. Scores tokens 0-100 with risk assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidadong2359](https://clawhub.ai/user/weidadong2359) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to query public meme-coin data sources, compare token momentum and liquidity, and produce scored signal summaries with risk labels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes live crypto API lookups and speculative token scoring that can produce unreliable or misleading trading signals. <br>
Mitigation: Treat outputs as informational only and independently verify token liquidity, holder concentration, and market data before acting. <br>
Risk: The skill auto-activates broadly and describes recurring polling every five minutes. <br>
Mitigation: Use the skill manually unless background polling is explicitly approved and scoped. <br>
Risk: The skill says to report strong signals to a creator or external party. <br>
Mitigation: Do not send reports externally unless the destination and contents are reviewed and explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidadong2359/meme-signal) <br>
- [DEXScreener latest token boosts API](https://api.dexscreener.com/token-boosts/latest/v1) <br>
- [DEXScreener token lookup API](https://api.dexscreener.com/latest/dex/tokens/TOKEN_ADDRESS) <br>
- [GeckoTerminal Solana trending pools API](https://api.geckoterminal.com/api/v2/networks/solana/trending_pools) <br>
- [Pump.fun latest coins API](https://frontend-api-v3.pump.fun/coins/latest) <br>
- [CoinGecko trending search API](https://api.coingecko.com/api/v3/search/trending) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown signal summaries with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores tokens from 0-100 and labels risk as low, medium, or high based on the skill's stated scoring rules.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
