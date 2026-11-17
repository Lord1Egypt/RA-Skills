## Description:

Provides NBA Playoffs coverage with schedules, scores, reminders, team stats, bracket visualization, predictions, watch information, and shareable flair images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bgoodwinstudio](https://clawhub.ai/user/bgoodwinstudio)

### License/Terms of Use:

MIT-0

## Use Case:

NBA fans and chat-group users use this skill to follow playoff schedules and scores, receive reminders, track brackets and predictions, find watch information, and generate shareable team flair.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated flair files can be written to a user-supplied output path.

Mitigation: Keep generated flair output inside a normal workspace or output folder.

Risk: NBA reminder and score-posting cron jobs may continue running after the user stops using the skill.

Mitigation: Review active OpenClaw tasks and use the documented removal command to remove NBA-related cron jobs and local config files.

Risk: Messages are sent through already configured chat channels.

Mitigation: Use only intended existing channels and do not provide new credentials to this skill.

## Reference(s):

- [NBA Teams Broadcast & Radio Reference](artifact/references/teams.md)
- [ESPN public NBA scoreboard API](https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Files, Shell commands, Guidance]

**Output Format:** [Markdown and plain text messages, local Markdown configuration files, scheduled reminders, and SVG flair images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ESPN public NBA data and existing configured messaging channels; no new API key is required.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
