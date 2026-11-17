## Description:

Exploits BTC/ETH correlation (beta=1.3) to trade ETH price-level markets when BTC makes a significant move. ETH tends to lag BTC moves, creating mispricing windows. Requires SIMMER_API_KEY and simmer-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and advanced trading agents use this skill to monitor Kalshi BTC and ETH price-level markets, estimate ETH fair value from BTC sentiment, and generate or execute constrained paper/live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests high-value trading credentials, including broad API access and a Solana private key for live trading.

Mitigation: Use limited-scope trading credentials where available, avoid exposing a full wallet private key unless necessary, and keep secrets out of shared logs or prompts.

Risk: Live mode can place real Kalshi trades using USDC.

Mitigation: Run in paper mode by default, use --live only after review, and keep max position size, max trades per run, and slippage limits conservative.

Risk: Dry-run execution is not fully read-only because market discovery can modify remote Simmer market state.

Mitigation: Test in an isolated account or workspace and review remote state changes before connecting production credentials.

Risk: The security verdict is suspicious and the skill depends on simmer-sdk for market access and trade execution.

Mitigation: Review carefully before installing and pin and review simmer-sdk before live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-crypto-correlation-trader)
- [Simmer skills homepage](https://simmer.markets/skills)
- [simmer-sdk PyPI package](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Text logs, JSON automaton reports, Markdown guidance, and Python/shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; live trading also requires SOLANA_PRIVATE_KEY and explicit --live execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
