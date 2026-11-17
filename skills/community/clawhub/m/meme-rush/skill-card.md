## Description:

Meme Rush helps agents query public Binance Web3 meme-token and topic data for launchpad lifecycle tracking, market-topic discovery, and filtered token analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awessh](https://clawhub.ai/user/awessh)

### License/Terms of Use:


## Use Case:

External agents and users use this skill to retrieve meme-token launchpad rankings, migration-stage data, hot-topic rankings, and token filtering signals for Solana and BSC markets. Outputs should be treated as informational market data, not trading recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake meme-token rankings, inflow signals, or topic narratives for financial advice.

Mitigation: Present outputs as informational market data and require users to make independent trading decisions.

Risk: Meme tokens can be illiquid, manipulated, scams, or total-loss assets, and the skill does not verify token legitimacy.

Mitigation: Encourage independent due diligence before acting on token data, including liquidity, holder concentration, dev activity, and external legitimacy checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awessh/skills/meme-rush)
- [Binance Web3 Meme Rush rank list API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/rank/list)
- [Binance Web3 Topic Rush rank list API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/social-rush/rank/list)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, guidance]

**Output Format:** [Markdown with API request examples and structured market-data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public token, topic, liquidity, holder-distribution, migration, and narrative fields returned by Binance Web3 APIs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
