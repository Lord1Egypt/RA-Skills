## Description:

Trades NBA player prop mispricings on Polymarket by detecting cross-stat consistency or divergence for the same player (Points, Rebounds, Assists O/U) and identifying outlier stats that disagree with the consensus direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to identify and optionally trade Polymarket NBA player prop markets whose points, rebounds, and assists prices diverge from same-player consensus. It defaults to paper trading and requires explicit live mode for real USDC trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real USDC trades.

Mitigation: Keep the default paper mode unless live trading risk is accepted, and cap account exposure independently of the skill.

Risk: The required trading API key can authorize market activity.

Mitigation: Use a dedicated, least-privilege Simmer/Polymarket key and protect it as a high-value credential.

Risk: Some stated financial safeguards are not fully enforced.

Mitigation: Do not rely on the documented minimum-volume or maximum-open-position safeguards until the implementation is fixed.

Risk: The trading SDK dependency is unpinned.

Mitigation: Prefer a pinned, reviewed version of simmer-sdk before installation or live execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-48h-player-prop-consistency-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Configuration]

**Output Format:** [Console text with market analysis, trade status, and Simmer/Polymarket API trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to simulated trading; live trading requires the --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release metadata; artifact frontmatter 1.0.0 and clawhub.json 0.0.2 differ)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
