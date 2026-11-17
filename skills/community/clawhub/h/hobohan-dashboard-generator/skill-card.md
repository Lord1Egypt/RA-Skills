## Description:

Generate self-contained HTML dashboards for memory logs, expense charts, and token usage. Run hourly via cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hohobohan](https://clawhub.ai/user/hohobohan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain local dashboards for memory logs, expense data, and token usage so private operational activity can be reviewed from generated HTML and JSON outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sets up persistent scheduled jobs and a local dashboard server that can expose comprehensive memory, ledger, and usage data.

Mitigation: Install only when a persistent local dashboard is intended, bind the server to localhost, restrict served directory permissions, and document stop and removal procedures for cron jobs and watchdogs.

Risk: The security evidence does not identify clear access controls for the served dashboard data.

Mitigation: Add authentication or another access gate before enabling access beyond a trusted local environment.

Risk: The skill runs external workspace scripts to generate and serve dashboard data.

Mitigation: Review the referenced scripts before deployment and limit their filesystem permissions to the dashboard and source data they require.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hohobohan/skills/hobohan-dashboard-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash commands plus HTML and JSON dashboard file descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or refreshes local dashboard files and runs a localhost dashboard server when configured.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
