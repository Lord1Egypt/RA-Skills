## Description:

Transform your OpenClaw workspace into personalized AI-powered podcast briefings with daily audio updates on work, priorities, and strategy across multiple briefing styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamjurgens](https://clawhub.ai/user/adamjurgens)

### License/Terms of Use:


## Use Case:

OpenClaw users and agent operators use this skill to turn workspace memory, job, heartbeat, and project files into private podcast briefings for daily or weekly review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace-derived briefing data is sent to a remote Superlore API when generating episodes.

Mitigation: Run a dry run first, review what will be transmitted, and enable scheduled runs only if recurring transmission is acceptable.

Risk: The setup wizard can persist the Superlore API key in a shell profile.

Mitigation: Prefer a temporary or manually managed API key, and avoid saving credentials to shell startup files unless that persistence is intended.

Risk: Scheduled cron jobs can repeatedly generate and send briefings without further prompting.

Mitigation: Review each generated cron command before activation and install only the schedules that match the user's data-sharing expectations.

Risk: Custom style names with shell metacharacters may affect command construction.

Mitigation: Use simple alphanumeric custom style names and inspect scheduled command output before running it.

## Reference(s):

- [Superlore API Reference](references/api.md)
- [Briefing Styles Reference](references/styles.md)
- [Superlore](https://superlore.ai)
- [Superlore API endpoint](https://superlore-api.onrender.com)
- [ClawHub skill page](https://clawhub.ai/adamjurgens/skills/openclaw-podcast)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated podcast episode links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create private Superlore podcast episodes from sanitized workspace briefing data and can emit OpenClaw cron commands for scheduled briefings.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
