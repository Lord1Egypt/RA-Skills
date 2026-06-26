## Description: <br>
NBA Tracker helps agents query NBA schedules, live scores, standings, player statistics, injuries, crunch-time game states, and optional calendar reminders using nba_api. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoruikun0531](https://clawhub.ai/user/luoruikun0531) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and sports-focused agent builders use this skill to add NBA viewing assistance, including team and player tracking, schedule lookup, live score checks, injury review, crunch-time alerts, and calendar reminder workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented Apple Calendar helper can create persistent local calendar events. <br>
Mitigation: Treat calendar writes as opt-in: preview the event title, date, time, and target calendar before execution and ask the user to confirm. <br>
Risk: The release depends on external Python packages and live NBA data endpoints. <br>
Mitigation: Pin dependencies in sensitive environments and handle throttling, network errors, and stale or delayed data explicitly. <br>
Risk: The artifact describes viewing assistance and notes that betting or prediction-market uses need lower-latency professional data. <br>
Mitigation: Use this skill for viewing and tracking workflows, and choose a professional real-time sports data source for betting, trading, or other latency-sensitive decisions. <br>


## Reference(s): <br>
- [NBA Tracker Skill Documentation](artifact/SKILL.md) <br>
- [NBA API Reference](artifact/API_REFERENCE.md) <br>
- [nba_api GitHub Repository](https://github.com/swar/nba_api) <br>
- [nba_api Documentation](https://github.com/swar/nba_api/tree/master/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live or cached NBA data returned through nba_api and optional local calendar event creation commands.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
