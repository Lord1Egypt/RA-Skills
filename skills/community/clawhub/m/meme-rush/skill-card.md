## Description: <br>
Meme Rush helps agents retrieve real-time meme-token launchpad rankings and AI-generated market topics from Binance Web3 endpoints across Solana and BSC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Awessh](https://clawhub.ai/user/Awessh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to inspect new, finalizing, and migrated meme tokens, discover market topics, and apply token filters such as liquidity, market cap, holder distribution, and developer activity. It is intended for informational market-data workflows, not trading execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meme-token rankings may be mistaken for financial advice. <br>
Mitigation: Present results as informational market data and avoid buy, sell, or hold recommendations. <br>
Risk: Users may expose wallet secrets or attempt to authorize trades while researching tokens. <br>
Mitigation: Do not request seed phrases, private keys, wallet credentials, or transaction authorization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Awessh/meme-rush) <br>
- [Publisher profile](https://clawhub.ai/user/Awessh) <br>
- [Meme Rush Rank List endpoint](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/rank/list) <br>
- [Topic Rush Rank List endpoint](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/social-rush/rank/list) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with API parameters, response-field descriptions, and inline curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Market-data guidance only; no credential handling or trading execution is described.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
