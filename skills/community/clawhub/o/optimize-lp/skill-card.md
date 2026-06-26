## Description: <br>
Get the optimal LP strategy for a token pair — recommends version (V2/V3/V4), fee tier, range width, and rebalance approach based on pair characteristics, historical data, and risk tolerance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and DeFi operators use this skill to compare Uniswap LP options for a token pair and receive a strategy covering version, fee tier, range width, expected returns, impermanent loss, and rebalance approach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LP recommendations may be incorrect, stale, or unsuitable for the user's position size, chain, time horizon, or risk tolerance. <br>
Mitigation: Require users to provide the token pair, chain, position size, time horizon, and risk tolerance, and independently review recommendations before depositing liquidity or making trades. <br>
Risk: Users may mistake strategy guidance for trade or liquidity execution. <br>
Mitigation: Present outputs as financial research only and make clear that this skill does not execute trades, access credentials, or deposit liquidity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/optimize-lp) <br>
- [Publisher profile](https://clawhub.ai/user/wpank) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown strategy recommendation with numeric estimates and risk assessment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides financial research and LP strategy guidance only; it does not execute trades or deposit liquidity.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
