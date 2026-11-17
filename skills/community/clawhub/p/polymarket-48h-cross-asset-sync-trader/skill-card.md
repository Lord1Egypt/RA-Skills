## Description:

Trades cross-asset correlation divergences in 5-minute crypto "Up or Down" markets on Polymarket by detecting outliers across BTC, ETH, SOL, DOGE, XRP, and BNB markets with overlapping time windows and sizing trades by conviction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to identify short-window cross-asset divergence opportunities in Polymarket crypto Up or Down markets and place simulated or live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that live-trading safeguards and documented risk limits do not fully match the code.

Mitigation: Review before installing, run in paper mode first, and do not enable live trading until the live-mode cache issue and advertised volume/open-position controls are fixed or independently verified.

Risk: The skill requires SIMMER_API_KEY, which can authorize trading activity.

Mitigation: Use a least-privilege key with tight account and spending limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-48h-cross-asset-sync-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text from trading runs, with configuration through environment variables and ClawHub tunables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless live mode is explicitly enabled.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
