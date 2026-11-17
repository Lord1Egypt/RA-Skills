## Description:

Tech/market trend weekly auto-report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to monitor AI, SaaS, Korean startup, and OpenClaw ecosystem trends and generate recurring weekly trend reports with highlights, category summaries, and watchlist items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create recurring report files and event records when run or scheduled.

Mitigation: Review the configured output paths and enable cron scheduling only when recurring writes are intended.

Risk: Generated trend reports may influence downstream automation in workspaces that react to report or event files.

Mitigation: Review generated reports and event records before connecting them to automated follow-up workflows.

## Reference(s):

- [Trend Radar ClawHub listing](https://clawhub.ai/mupengi-bot/skills/mupeng-trend-radar)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON event records, keyword configuration examples, and cron command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write weekly report files under memory/research and event records under events when run or scheduled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
