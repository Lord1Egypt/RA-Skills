## Description:

Trades structural arbitrage between Overwatch BO3 series winner markets and individual game winner markets on Polymarket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External trading-agent users use this skill to monitor Overwatch best-of-3 Polymarket bundles, compare series-winner prices against individual game-winner probabilities, and optionally place paper or live trades based on detected inconsistencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the release suspicious because live-trading safeguards are under-enforced.

Mitigation: Keep the skill in paper mode until the risk checks are reviewed, SDK dependency is pinned, and a tightly scoped limited API key is configured.

Risk: Running with --live can place real-money Polymarket orders.

Mitigation: Use --live only after verifying thresholds, position limits, spread checks, and max open-position settings for the intended account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-bundle-overwatch-bo3-trader)
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/)
- [Simmer SDK on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text and trading actions through the configured Simmer venue]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless run with --live.]

## Skill Version(s):

0.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
