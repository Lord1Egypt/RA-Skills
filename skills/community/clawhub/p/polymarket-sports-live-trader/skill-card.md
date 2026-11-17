## Description:

Trades Polymarket prediction markets on sports championships, tournament outcomes, MVP awards, transfer windows, and season milestones using configurable sports-market signals and execution safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run or adapt a Polymarket sports trading agent that discovers sports markets, sizes positions from simple probability thresholds, and can execute paper or live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money Polymarket orders.

Mitigation: Use paper mode by default and enable live mode only after reviewing configuration, credentials, and position limits.

Risk: Documented safeguards do not fully match the implemented defaults and enforcement.

Mitigation: Correct and test volume filtering, default values, final position-size caps, date parsing, and open-position accounting before relying on the skill for live trading.

Risk: The dependency is not pinned in the artifact configuration.

Mitigation: Pin and review the Simmer SDK dependency before installation in controlled or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-sports-live-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)
- [ESPN scoreboard API reference URL pattern](https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Console text, Python execution behavior, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket execution requires an explicit --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
