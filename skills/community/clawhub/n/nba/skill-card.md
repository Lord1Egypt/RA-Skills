## Description: <br>
Get today's NBA game schedule, live scores, final results, and current season standings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer current NBA schedule, score, result, and standings questions with live public sports data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Results depend on live outbound requests to NBA and StatMuse, so responses can fail or become stale when those services are unavailable. <br>
Mitigation: Tell users when live data cannot be fetched and direct them to the NBA schedule or StatMuse pages as fallbacks. <br>
Risk: The StatMuse standings parser may break if StatMuse changes its page layout. <br>
Mitigation: Verify standings output before presenting it and fall back to direct StatMuse or NBA standings links when parsing fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/nba) <br>
- [NBA live scoreboard data](https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json) <br>
- [NBA schedule](https://www.nba.com/schedule) <br>
- [StatMuse NBA](https://www.statmuse.com/nba) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands and plain-text score or standings output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public NBA and StatMuse web data; no API key or external dependency installation is required.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
