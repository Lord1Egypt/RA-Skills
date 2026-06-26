## Description: <br>
Access a Jira workspace using provided email and API token credentials to list, create, comment on, and transition Jira issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brajesh9373](https://clawhub.ai/user/brajesh9373) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to operate Jira issues from an agent session, including JQL searches, issue creation, status transitions, and comments. It is intended for users who intentionally want the agent connected to the configured Jira workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is configured around a specific Atlassian tenant and account email. <br>
Mitigation: Install it only for that intended workspace, or edit the configuration examples before use so they point to the user's own Jira tenant and account. <br>
Risk: The skill requires Jira API credentials. <br>
Mitigation: Use a dedicated low-permission API token and store it in environment variables or a secret store rather than committing it or placing it in shell history. <br>
Risk: The skill can create issues, transition statuses, and post comments in a live Jira workspace. <br>
Mitigation: Require explicit user approval before running mutating commands such as create, transition, or comment. <br>


## Reference(s): <br>
- [Jira REST API documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/) <br>
- [ClawHub release page](https://clawhub.ai/brajesh9373/jira-access) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Jira environment variables and the Python requests dependency.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
