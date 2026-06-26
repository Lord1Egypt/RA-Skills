## Description: <br>
Queries football match schedules and league standings for supported leagues such as the Chinese Super League, English Premier League, Serie A, Bundesliga, Ligue 1, Spanish second division, and Scottish Premiership using Juhe's football API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query football schedules, match results, and league tables for supported leagues, then present the returned Juhe football data clearly to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required Juhe API key could be exposed through command-line arguments, logs, shell history, or shared environment files. <br>
Mitigation: Prefer the JUHE_FOOTBALL_KEY environment variable, avoid logging the key, do not share shell history or .env files containing it, and rotate the key if exposure is suspected. <br>
Risk: Juhe API quota limits or billing policy changes can interrupt lookups or create unexpected usage pressure. <br>
Mitigation: Monitor Juhe quota usage, handle quota errors clearly, and confirm the active Juhe plan before relying on the skill for repeated queries. <br>
Risk: The artifact uses HTTP API endpoints, which may expose requests or API keys if used over untrusted networks. <br>
Mitigation: Use an HTTPS endpoint if Juhe supports it, and avoid running key-bearing requests over networks that are not trusted. <br>


## Reference(s): <br>
- [Juhe Football League API documentation](https://www.juhe.cn/docs/api/id/90) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JUHE_FOOTBALL_KEY API key and returns formatted schedules or standings from Juhe API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
