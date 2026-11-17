## Description:

Trades Polymarket coffee markets using Brazil frost-window timing, harvest-cycle awareness, and ENSO phase as seasonal conviction signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-automation users use this skill to scan coffee-related Polymarket markets, compute seasonal YES/NO trade conviction, and run paper trades by default or live trades when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real USDC trades while documented safeguards may not reliably enforce all advertised limits.

Mitigation: Use paper mode unless live trading is explicitly intended; for live use, apply a tightly limited API key and verify position, portfolio, volume, and spread limits before deployment.

Risk: A high-value SIMMER_API_KEY is required for trading authority.

Mitigation: Store the key as a secret, scope or cap it where possible, rotate it regularly, and avoid exposing it in logs or skill artifacts.

Risk: The ENSO phase is manually configured and can become stale, affecting trade conviction.

Mitigation: Review SIMMER_ENSO_PHASE before live operation and update it from a trusted climate outlook source on the cadence required by the strategy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-coffee-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Console logs and agent guidance with trade side, size, mode, and reasoning]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paper trading is the default; live trading requires the --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
