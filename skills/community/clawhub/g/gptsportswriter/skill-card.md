## Description: <br>
GPTSportswriter generates sports betting research reports from live odds, matchup context, and public or news sources, with premium API-backed and free public-source workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[normandmickey](https://clawhub.ai/user/normandmickey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to produce structured betting research, matchup breakdowns, and sportsbook-style summaries from current odds and public or news context. It is intended for research and summaries, not for placing bets or claiming guaranteed outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The email helper can send a generated betting report to a fixed personal Gmail recipient after loading the workspace environment. <br>
Mitigation: Review or disable scripts/send_daily_report.sh before installing; prefer a version that asks for the recipient and loads only required secrets. <br>
Risk: Generated betting reports can be misleading if users treat stale odds, source disagreement, or line movement as guaranteed outcomes. <br>
Mitigation: Require current odds checks, include uncertainty and line-sensitivity notes, and avoid claims of guaranteed wins. <br>


## Reference(s): <br>
- [GPTSportswriter on ClawHub](https://clawhub.ai/normandmickey/gptsportswriter) <br>
- [The Odds API sports endpoint](https://api.the-odds-api.com/v4/sports) <br>
- [Covers MLB matchups](https://www.covers.com/sport/baseball/mlb/matchups) <br>
- [Covers NBA matchups](https://www.covers.com/sport/basketball/nba/matchups) <br>
- [Covers NHL matchups](https://www.covers.com/sport/hockey/nhl/matchups) <br>
- [Covers EPL matchups](https://www.covers.com/sport/soccer/england-premier-league/matchups) <br>
- [wttr.in weather service](https://wttr.in/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown betting research report with optional JSON outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some workflows require odds or news API credentials; free mode uses public sources and may be less current.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
