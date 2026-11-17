## Description:

Trades commodity markets based on extreme weather signals by using temperature markets to identify potential energy demand spikes or crop disruption that commodity markets may not have priced in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor Polymarket weather and commodity markets, compute weather stress signals, and place simulated or live commodity trades when configured. It is intended for users who understand prediction-market trading risk and can review live-trading controls before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-trading safeguards are weaker than documented and could expose real funds to unintended risk.

Mitigation: Keep the skill in paper mode unless the SDK dependency is pinned and volume, slippage, context, and account-position limits are enforced against real account state.

Risk: The skill requires a trading API key with authority to place orders.

Mitigation: Use a restricted API key and small limits for any live testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-macro-weather-commodity-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The trading script defaults to paper mode and requires an explicit live flag for Polymarket execution.]

## Skill Version(s):

0.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
