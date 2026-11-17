## Description:

Manage Jira issues, transitions, comments, assignments, and worklogs through the Jira Cloud REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weihezhai](https://clawhub.ai/user/weihezhai)

### License/Terms of Use:


## Use Case:

Developers and project teams use this skill to search, inspect, create, update, assign, transition, comment on, and track worklogs for Jira issues from an agent-assisted command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Jira credentials or worklog-derived data could be exposed through weak endpoint validation or unintended metrics export.

Mitigation: Use an HTTPS Jira URL, avoid untrusted Jira endpoints, leave JIRA_METRICS_URL unset unless export is intended, and review or remove the metrics command before installation.

Risk: A broadly scoped Jira API token could increase impact if exposed or misused.

Mitigation: Use a low-privilege Jira API token and rotate it if it may have been sent over HTTP or used against an untrusted endpoint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weihezhai/skills/jira-m)
- [Jira Cloud REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Jira Cloud credentials in environment variables and local command-line tools including curl, jq, bc, and python3.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
