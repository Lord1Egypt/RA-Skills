## Description:

Trades structural mispricings in sports over/under markets by reconstructing implied probability curves across multiple line values for the same game and detecting monotonicity violations and tennis set-vs-match inconsistencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to find sports over/under pricing inconsistencies on Polymarket, rank candidate curve violations, and run the strategy in paper mode or explicit live mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-trading safeguards do not fully enforce the limits the skill advertises.

Mitigation: Review carefully before installing, use paper mode first, and do not rely on the advertised position-count, minimum-volume, or context-risk safeguards until they are fixed or enforced server-side.

Risk: Live mode can place real Polymarket trades using a high-value trading credential.

Mitigation: Use the least-privileged or sandbox trading key available and enable live mode only after reviewing the strategy and configured limits.

## Reference(s):

- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)
- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-24h-sports-line-curve-trader)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Console text with configurable paper or live trading execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless --live is supplied.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
