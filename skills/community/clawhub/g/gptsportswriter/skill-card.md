## Description:

GPTSportswriter generates sports betting research reports from live odds, matchup context, and public or news sources, with premium API-backed and free public-source modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[normandmickey](https://clawhub.ai/user/normandmickey)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to assemble current sports betting research reports, matchup breakdowns, and cautious best-bet summaries. It is for research summaries, not bet placement or guaranteed outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The email helper can send generated reports to a fixed external Gmail address while loading broad workspace environment variables.

Mitigation: Do not run scripts/send_daily_report.sh until the recipient, message content, and available environment variables have been reviewed and restricted.

Risk: Sports betting recommendations can become misleading when odds, injuries, weather, or public-source snapshots are stale.

Mitigation: Re-run data collection close to the event, compare current lines across sources, and keep uncertainty and line sensitivity visible in the report.

Risk: Free-mode public-source extraction can be incomplete when pages change or paid API keys are unavailable.

Mitigation: Treat free-mode output as research context, verify current odds before use, and avoid forcing picks when source coverage is thin.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/normandmickey/skills/gptsportswriter)
- [The Odds API sports endpoint](https://api.the-odds-api.com/v4/sports)
- [Covers MLB matchups](https://www.covers.com/sport/baseball/mlb/matchups)
- [Covers NBA matchups](https://www.covers.com/sport/basketball/nba/matchups)
- [Covers NHL matchups](https://www.covers.com/sport/hockey/nhl/matchups)
- [Covers Premier League matchups](https://www.covers.com/sport/soccer/england-premier-league/matchups)
- [wttr.in weather service](https://wttr.in/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Structured Markdown reports, JSON data payloads, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on current odds, news context, configured API keys, and public-source availability; free-mode odds may be stale or incomplete.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
