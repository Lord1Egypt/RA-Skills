## Description:

Trades ETH price markets on Kalshi using on-chain gas prices as a bullish/bearish signal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to evaluate and optionally trade Kalshi ETH price markets using configurable gas-regime signals. It is intended to run in dry-run mode by default, with live trading enabled only by an explicit flag and funded credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can execute real-money Kalshi trades with high-value credentials.

Mitigation: Keep the skill in dry-run mode until reviewed, and use restricted, low-balance credentials when enabling --live.

Risk: The implemented strategy and safety boundaries do not match the documentation closely enough for real-money use.

Mitigation: Review the exact simmer-sdk version and validate the strategy behavior before funding or scheduling live runs.

Risk: The current code does not actually fetch on-chain gas prices.

Mitigation: Add or verify a reliable gas-price source before relying on the signal for live trading.

Risk: The skill may sell unrelated ETH positions in the connected account.

Mitigation: Use an isolated account or wallet, keep balances low, and inspect positions before enabling live execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-eth-gas-correlation-trader)
- [Simmer Markets skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls]

**Output Format:** [Plain text console output with optional JSON automaton status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; live trading requires --live plus SIMMER_API_KEY and SOLANA_PRIVATE_KEY.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
