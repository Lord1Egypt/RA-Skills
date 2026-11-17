## Description:

Trades ETH price markets on Kalshi using the 4% staking yield as a fundamental price floor. When markets underprice ETH relative to the yield-implied floor, buy YES. Requires SIMMER_API_KEY and simmer-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to evaluate Kalshi ETH price markets against a staking-yield floor model, surface trade signals, and optionally execute live trades when explicitly run with the live flag.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can execute real-money Kalshi trades and affect ETH positions.

Mitigation: Review the live-trading flow before use, keep the default dry-run mode until ready, and require the explicit --live flag for real trades.

Risk: SIMMER_API_KEY and SOLANA_PRIVATE_KEY are high-value credentials.

Mitigation: Use narrowly limited credentials, prefer a dedicated low-balance wallet and restricted trading account, and avoid exposing SOLANA_PRIVATE_KEY for dry-run use.

Risk: The trading model uses configurable assumptions such as staking yield, base ETH price, entry edge, slippage, and position size.

Mitigation: Validate and tune risk parameters before live operation, including max position size, max trades per run, slippage, and liquidity settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-eth-staking-yield-trader)
- [Simmer Markets skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, JSON, API calls, Guidance]

**Output Format:** [Terminal text with an optional automaton JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to dry-run mode; live trading requires the explicit --live flag and configured credentials.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
