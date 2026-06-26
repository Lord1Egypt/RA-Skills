## Description: <br>
Daily MLB baseball scores, box scores, starting pitchers, and injury reports for your favourite team. Covers spring training, regular season, and playoffs. Runs on a schedule or on demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremydouglaslaw-ui](https://clawhub.ai/user/jeremydouglaslaw-ui) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and baseball fans use this skill to receive scheduled or on-demand MLB team briefings with recent scores, upcoming game details, starting pitchers, and injury reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer creates a local Python virtual environment and installs Python dependencies. <br>
Mitigation: Install only in environments where local dependency installation is acceptable, and review the setup script before deployment. <br>
Risk: The runtime reads the configured team and timezone from the OpenClaw configuration and makes outbound requests to the MLB Stats API. <br>
Mitigation: Configure only the intended team and timezone, and use the skill only in channels where daily baseball updates are wanted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jeremydouglaslaw-ui/mlb-daily-scores) <br>
- [ClawHub Skill Homepage](https://clawhub.ai/skills?focus=search&q=mlb-daily-scores) <br>
- [MLB Stats API](https://statsapi.mlb.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the fetch script, formatted by the agent into concise Markdown or chat text for scheduled and on-demand delivery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit HEARTBEAT_OK when no game or injury data is available, so scheduled runs can suppress empty updates.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
