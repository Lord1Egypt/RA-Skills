## Description:

Trades structural mispricings in sports over/under markets by reconstructing the implied probability curve across multiple O/U line values for the same game and detecting monotonicity violations and set-vs-match inconsistencies in tennis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to scan Polymarket sports over/under markets for implied probability curve violations and optionally place paper or live trades through Simmer. It is intended for review-led deployment with explicit live-mode activation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money trades while advertised risk controls may be weak or not enforced.

Mitigation: Use paper trading by default and require manual review before enabling --live.

Risk: Market and execution safeguards may not fail closed in every live trading path.

Mitigation: Before live use, verify min-volume enforcement, fail-closed context checks, and position plus pending-order accounting.

Risk: The trading credential can authorize financial actions.

Mitigation: Use a SIMMER_API_KEY scoped to the minimum trading authority acceptable for the deployment.

Risk: Unpinned dependencies can change runtime behavior.

Mitigation: Add a pinned dependency or lockfile before production live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-48h-sports-line-curve-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API Calls, Configuration]

**Output Format:** [Console text logs with Simmer trade requests and tunable configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trades require the --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
