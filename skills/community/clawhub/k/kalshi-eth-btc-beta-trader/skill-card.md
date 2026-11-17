## Description:

Trades ETH price markets on Kalshi by exploiting the 1.3x beta relationship between ETH and BTC. When BTC odds shift, ETH markets lag behind -- this skill captures the catch-up. Requires SIMMER_API_KEY and simmer-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and advanced trading agents use this skill to discover Kalshi ETH and BTC markets through Simmer, compare ETH market prices against a static ETH/BTC beta model, and produce dry-run or live trading actions subject to configured safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires high-value trading credentials, including a Simmer API key and a Solana private key for live trading.

Mitigation: Use a dedicated low-balance trading wallet, avoid providing SOLANA_PRIVATE_KEY for dry-run or read-only use, and install only after reviewing the dependency and artifact.

Risk: Live mode can execute real Kalshi trades using USDC.

Mitigation: Run in the default dry-run mode first, pass --live only after manual review, and keep position size, trade count, slippage, and liquidity tunables conservative.

Risk: Default runs may import markets into the user's Simmer account even when no trades are placed.

Mitigation: Use the skill only where authenticated account changes are acceptable, and review or pin simmer-sdk before live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-eth-btc-beta-trader)
- [Simmer skills homepage](https://simmer.markets/skills)
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/)
- [Simmer SDK repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, trading actions]

**Output Format:** [Console text with optional JSON automaton reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print configuration, current ETH positions, dry-run trade opportunities, executed trade status, skip reasons, and managed automaton summaries.]

## Skill Version(s):

1.0.8 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
