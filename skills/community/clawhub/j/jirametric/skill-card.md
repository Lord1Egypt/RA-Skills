## Description:

Retrieve and analyze Jira worklog metrics by user, issue, or date ranges through Jira Cloud REST API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weihezhai](https://clawhub.ai/user/weihezhai)

### License/Terms of Use:


## Use Case:

Developers and project operators use this skill to query Jira issues, manage worklogs, and summarize logged hours by user, issue, or date range from Jira Cloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Jira worklog-derived metrics can be sent to a URL set in JIRA_METRICS_URL by an undocumented metrics command.

Mitigation: Do not set JIRA_METRICS_URL unless that destination is intended and trusted; remove, document, or constrain the metrics command before routine use.

Risk: The skill uses Jira credentials and may query broadly when JIRA_BOARD is empty.

Mitigation: Use a least-privilege Jira API token, set JIRA_URL only to a trusted HTTPS Jira tenant, and configure JIRA_BOARD when project-limited access is intended.

## Reference(s):

- [Jira Cloud REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [ClawHub skill page](https://clawhub.ai/weihezhai/skills/jirametric)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON outputs from worklog queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, bc, python3, JIRA_URL, JIRA_EMAIL, and JIRA_API_TOKEN; JIRA_BOARD can optionally limit project scope.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
