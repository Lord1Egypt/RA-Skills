## Description:

Trades structural inconsistencies across correlated NBA game markets on Polymarket by grouping moneyline, spread, full-game and first-half totals, and first-half moneyline markets for the same game to detect cross-market mispricings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this skill to scan related NBA prediction markets, identify structural inconsistencies, and propose or place threshold-gated Polymarket trades. It defaults to paper trading and requires an explicit live mode for real USDC exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can expose more funds than users expect because safeguards are under-enforced.

Mitigation: Use paper mode by default; enable live mode only with a tightly limited API key, small balances, and reviewed position limits.

Risk: Volume, position-count, and fail-closed context checks may not be strong enough for unattended live use.

Mitigation: Fix and test those checks before live deployment, and block trading when required market context or risk checks are unavailable.

Risk: The SIMMER_API_KEY grants trading authority and is a high-value credential.

Mitigation: Store the key as a managed secret, scope it as narrowly as possible, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-24h-nba-game-structure-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python execution commands, tunable configuration, and trading rationale text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit paper or live trade actions through the configured Simmer venue; live trading requires an explicit flag and a SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
