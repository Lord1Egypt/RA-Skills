## Description: <br>
Money Toolkit helps agents analyze crypto arbitrage, DeFi yields, airdrop opportunities, compound returns, and gas-cost savings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawto](https://clawhub.ai/user/clawto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect public crypto market and yield data, compare opportunities, and run basic financial planning calculations. Outputs should be treated as informational support rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market, APY, and gas data can be stale, unavailable, or inaccurate because the skill queries public third-party endpoints. <br>
Mitigation: Verify figures with independent sources before acting and treat endpoint failures or missing data as inconclusive. <br>
Risk: Crypto arbitrage, DeFi yield, and financial planning outputs may be mistaken for investment advice. <br>
Mitigation: Use outputs only as informational analysis and require human review before financial decisions. <br>
Risk: Entering wallet seed phrases, private keys, exchange credentials, or other secrets would create avoidable exposure. <br>
Mitigation: Do not provide secrets to the skill; use read-only public data and separate credentialed trading or wallet workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawto/money-toolkit) <br>
- [DeFiLlama Yields](https://defillama.com/yields) <br>
- [CoinGecko Simple Price API](https://api.coingecko.com/api/v3/simple/price) <br>
- [Binance Spot Ticker API](https://api.binance.com/api/v3/ticker/price) <br>
- [OKX Market Ticker API](https://www.okx.com/api/v5/market/ticker) <br>
- [Bybit Market Tickers API](https://api.bybit.com/v5/market/tickers) <br>
- [PublicNode RPC endpoints](https://ethereum-rpc.publicnode.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market prices, APY rankings, gas-cost estimates, calculation results, and cautions about data volatility.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
