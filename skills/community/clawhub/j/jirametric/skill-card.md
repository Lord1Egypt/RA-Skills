## Description: <br>
Retrieve and analyze Jira worklog metrics by user, issue, or date range, with supporting commands for Jira issue search, updates, assignment, comments, creation, and work logging through the Jira Cloud REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weihezhai](https://clawhub.ai/user/weihezhai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, project leads, and delivery teams use this skill to query Jira issues, update issue records, log work, and summarize worklog hours for personal, per-day, or per-issue reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Jira issues and worklogs, including transitions, assignment, comments, issue creation, and work logging. <br>
Mitigation: Use a least-privilege Jira API token and require manual approval before running write commands. <br>
Risk: Worklog-derived metrics can be posted to a URL configured through JIRA_METRICS_URL. <br>
Mitigation: Leave JIRA_METRICS_URL unset unless that destination is intentional and approved. <br>
Risk: Unscoped Jira queries may search across more projects than intended. <br>
Mitigation: Set JIRA_BOARD to explicit project keys before use. <br>


## Reference(s): <br>
- [Atlassian Jira Cloud REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/) <br>
- [Jira Metric on ClawHub](https://clawhub.ai/weihezhai/jirametric) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Jira Cloud credentials and local curl, jq, bc, and python3 dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
