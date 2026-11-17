## Description:

Trades NBA player prop mispricings on Polymarket by detecting cross-stat consistency or divergence for the same player and identifying outlier stats that disagree with the consensus direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to scan NBA player prop markets, group related player statistics, and produce paper or live trade actions when cross-stat consistency signals meet configured thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live Polymarket trades when run with --live and valid trading credentials.

Mitigation: Keep paper mode unless intentionally trading, use a restricted API key, and limit account balance exposure.

Risk: Advertised volume, open-position, and context safeguards may be weaker or incomplete.

Mitigation: Review and modify the code before relying on those controls as complete risk limits.

Risk: The skill depends on simmer-sdk for market access and trade execution.

Mitigation: Verify the SDK package and version before granting credentials or enabling live execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-24h-player-prop-consistency-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, API calls]

**Output Format:** [Markdown guidance, Python code, JSON configuration, and console status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can place paper trades by default and live Polymarket trades only when run with --live and valid credentials.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
