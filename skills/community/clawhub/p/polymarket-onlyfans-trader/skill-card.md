## Description:

Trades Polymarket markets on OnlyFans using structural signals for celebrity join events, platform ban markets, and creator earnings seasonality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover OnlyFans-related Polymarket markets, size paper trades by configurable thresholds, and optionally execute live trades after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades using the configured trading credential.

Mitigation: Keep the skill in paper mode until the strategy, SDK dependency, and account exposure are reviewed; use live mode only when real USDC risk is accepted.

Risk: Advertised safeguards and market scoping may not fully constrain live trades.

Mitigation: Review candidate markets and tune maximum position, volume, spread, days-to-resolution, and open-position limits before any live run.

Risk: Low-volume markets, generic OnlyFans searches, and repeated runs may create exposure beyond the user's intent.

Mitigation: Use small limits, monitor console output and account positions, and avoid unattended live automation unless operational controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-onlyfans-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text console output with configurable environment parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper mode unless live trading is explicitly enabled.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
