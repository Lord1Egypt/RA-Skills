## Description: <br>
Manage Jira issues, transitions, and worklogs via the Jira Cloud REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weihezhai](https://clawhub.ai/user/weihezhai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and project teams use this skill to search, view, create, assign, comment on, transition, and open Jira issues from shell commands. They can also log work hours and generate JSON worklog summaries for integration with other tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The metrics command can send Jira worklog summaries to any URL configured in JIRA_METRICS_URL. <br>
Mitigation: Leave JIRA_METRICS_URL unset unless export is intentional, and verify the destination and data handling before running metrics. <br>
Risk: The skill can perform write actions in Jira, including status changes, comments, assignments, issue creation, and logged hours. <br>
Mitigation: Use a least-privilege Jira API token and review each write command and target issue before execution. <br>


## Reference(s): <br>
- [ClawHub Jira skill page](https://clawhub.ai/weihezhai/jira-m) <br>
- [Jira Cloud REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/) <br>
- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown documentation with shell command examples and command output as text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, bc, python3, and Jira credentials in environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
