## Description:

Trade Polymarket SOL and crypto prediction markets using live Solana TPS, priority fees, DEX volume, and epoch data as on-chain signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chokle](https://clawhub.ai/user/chokle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this skill to collect Solana on-chain activity signals, identify active SOL, BTC, ETH, and crypto prediction markets, and optionally execute Simmer trades based on a composite bullish, neutral, or bearish signal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring automated live trading can place real trades on a schedule using SIMMER_API_KEY with under-disclosed risk controls.

Mitigation: Use a narrowly scoped and revocable SIMMER_API_KEY, set account-side spending limits, verify or disable the cron live-trading automation, and run in dry-run mode before enabling live execution.

Risk: The release security guidance calls out incomplete dependency pinning, live-trade confirmation, fail-closed safeguards, and cumulative loss limits.

Mitigation: Pin dependencies, require explicit confirmation for live trading where practical, prefer fail-closed behavior when signal or context checks fail, and add cumulative loss limits before relying on unattended operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chokle/skills/polymarket-solana-onchain)
- [Simmer docs](https://docs.simmer.markets)
- [Solana RPC docs](https://docs.solana.com/api/http)
- [Jupiter stats API](https://stats.jup.ag)
- [Helius RPC](https://helius.dev)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown instructions, Python code, command-line output, and optional JSON automaton reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in signal-only, dry-run, or live-trading modes; live mode may execute trades through Simmer.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
