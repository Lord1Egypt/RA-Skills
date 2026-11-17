## Description:

Trades F1 Drivers Championship markets on Kalshi using teammate anti-correlation, where structurally linked teammate probabilities can create relative mispricings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to identify and optionally trade Kalshi F1 Drivers Championship teammate-pair mispricings. It defaults to dry-run mode and requires explicit live execution before it can place real-money trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real-money trades when run with --live.

Mitigation: Keep dry-run workflows separate from live execution, require an explicit live flag, and review position limits before enabling live trading.

Risk: The skill asks for a raw Solana private key and trading credentials.

Mitigation: Use a dedicated low-value wallet, narrowly scoped or revocable trading credentials, and avoid provisioning wallet keys for dry-run use.

Risk: Live trading depends on the external simmer-sdk package.

Mitigation: Pin and review the simmer-sdk dependency before live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-f1-teammate-anti-trader)
- [Simmer Markets skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Console text with optional automaton JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can show dry-run opportunities, positions, configuration, trade attempts, executed trades, skipped trades, and tunable risk settings.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
