## Description:

Exploits price lag between ESPN real-time scores and Polymarket sports markets, using Gaussian win-probability models for NBA/NFL/NHL and Poisson models for soccer to identify trades when model probability diverges from market price by more than 10%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this automaton to monitor live sports scores, calculate model-based fair odds, and optionally place Polymarket trades when a configured divergence threshold is met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place repeated real-money trades with weak safety controls.

Mitigation: Use paper trading credentials and the default simulation venue unless server-side trade limits, dependency pinning, fail-closed market-context checks, and explicit live-mode confirmation are in place.

Risk: A trading credential may expose more trading authority or funds than intended.

Mitigation: Use a key with only the trading authority and funds you are prepared to risk.

Risk: Market-context checks can be unavailable during execution.

Mitigation: Treat unavailable market context as a reason to skip live trades before enabling real-money mode.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/mibayy/skills/polymarket-sports-live)
- [ESPN NBA scoreboard API endpoint](https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard)
- [ESPN NFL scoreboard API endpoint](https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard)
- [ESPN NHL scoreboard API endpoint](https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard)
- [ESPN EPL scoreboard API endpoint](https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard)
- [ESPN MLS scoreboard API endpoint](https://site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown guidance with bash commands and runtime log output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; dry-run is the default unless --live is passed.]

## Skill Version(s):

2.0.5 (source: server release metadata, clawhub.json, and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
