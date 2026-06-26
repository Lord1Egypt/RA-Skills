## Description: <br>
Provides NBA Playoffs coverage with schedules, scores, reminders, team stats, bracket visualization, predictions, watch information, and shareable team flair images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bgoodwinstudio](https://clawhub.ai/user/bgoodwinstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
NBA fans use this skill to follow playoff games in their configured messaging channel, including reminders, scores, brackets, watch information, prediction tracking, and shareable team flair. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill posts scheduled NBA reminders and score updates to the user's configured messaging channel. <br>
Mitigation: Install only for channels where those messages are wanted, review active jobs with openclaw tasks, and remove them with remove nba when no longer needed. <br>
Risk: The skill writes local NBA configuration and prediction files in the workspace. <br>
Mitigation: Review the generated local files and use remove nba to delete NBA-related cron jobs and config files. <br>


## Reference(s): <br>
- [ClawHub NBA Playoffs release page](https://clawhub.ai/bgoodwinstudio/nba-playoffs) <br>
- [ESPN public NBA scoreboard API](https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard) <br>
- [NBA Teams Broadcast & Radio Reference](references/teams.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown and chat messages with optional SVG flair files and local markdown configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May schedule reminder and score-update tasks through OpenClaw and write local NBA prediction and configuration files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
