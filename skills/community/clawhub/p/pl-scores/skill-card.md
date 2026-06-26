## Description: <br>
Get live Premier League football scores, goal scorers, bookings, and broadcast channels via the ESPN API for English top-flight matches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stigg86](https://clawhub.ai/user/stigg86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Premier League score, result, scorer, booking, and US broadcast-channel questions from live or recent ESPN match data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes an outbound request to ESPN for public Premier League data, so results depend on network availability and ESPN's data freshness. <br>
Mitigation: Use it only where outbound access to ESPN is acceptable, and treat live scores, bookings, and broadcast details as ESPN-sourced data that may need confirmation for high-stakes uses. <br>


## Reference(s): <br>
- [ESPN Premier League scoreboard API](https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard) <br>
- [ClawHub release page](https://clawhub.ai/stigg86/pl-scores) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text match summaries with scores, status, scorers, bookings, and broadcast channel details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires internet access to fetch public ESPN Premier League data; no credentials are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
