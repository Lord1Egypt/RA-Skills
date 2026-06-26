## Description: <br>
Trades ETH price markets on Kalshi using a post-merge deflation thesis, with Simmer credentials and simmer-sdk required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and traders can use this skill to run a configurable dry-run or live ETH price-market strategy on Kalshi through Simmer. It discovers ETH markets, estimates fair probability from a deflation thesis, and proposes or executes bounded trades when configured for live mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can execute real trades and spend USDC using trading and wallet credentials. <br>
Mitigation: Run dry-run first, keep scheduled automation disabled until intentionally configured, and use --live only after reviewing position, trade-count, slippage, and liquidity limits. <br>
Risk: The skill requires high-value SIMMER_API_KEY and SOLANA_PRIVATE_KEY credentials. <br>
Mitigation: Use a scoped API key and a limited funded wallet, avoid main wallets or broad credentials, and rotate secrets if exposure is suspected. <br>
Risk: Trading behavior depends on simmer-sdk and external market data. <br>
Mitigation: Review or pin simmer-sdk before enabling live mode and verify market context, liquidity, and slippage settings before funding trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-eth-merge-momentum-trader) <br>
- [Simmer skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [Console text with optional JSON automaton reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is the default; live trading requires an explicit --live flag and configured credentials.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
