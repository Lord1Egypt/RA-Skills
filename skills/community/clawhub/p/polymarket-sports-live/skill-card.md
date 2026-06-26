## Description: <br>
Exploits price lag between ESPN real-time scores and Polymarket sports markets, using sport-specific probability models to calculate fair odds and identify trades when model probability diverges more than 10% from market price. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this automaton to monitor live sports games, compare model-derived probabilities with Polymarket prices, and produce dry-run signals or live trades through SimmerClient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place repeated real-money trades without a final confirmation or overall exposure cap. <br>
Mitigation: Keep the default dry-run or simulated venue until tested, use a limited API key if possible, set a small SPORTS_TRADE_SIZE, confirm whether the automaton is live or simulated, and monitor or disable the cron job if continuous trading is not intended. <br>


## Reference(s): <br>
- [Polymarket Sports Live ClawHub listing](https://clawhub.ai/Mibayy/polymarket-sports-live) <br>
- [Mibayy publisher profile](https://clawhub.ai/user/Mibayy) <br>
- [ESPN NBA scoreboard endpoint](https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard) <br>
- [ESPN NFL scoreboard endpoint](https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard) <br>
- [ESPN NHL scoreboard endpoint](https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard) <br>
- [ESPN EPL scoreboard endpoint](https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard) <br>
- [ESPN MLS scoreboard endpoint](https://site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Console log text with optional SimmerClient trading API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is the default; live mode places trades through SimmerClient when enabled.] <br>

## Skill Version(s): <br>
2.0.5 (source: server release metadata, clawhub.json, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
