## Description: <br>
Jira API integration with managed OAuth for searching issues with JQL, creating and updating issues, and managing projects and transitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and support teams use this skill to interact with Jira Cloud issues, projects, comments, users, metadata, and workflow transitions through Maton-managed OAuth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and user-directed Jira access, so credentials or connected Jira data could be exposed if used in shared logs, transcripts, or terminals. <br>
Mitigation: Keep MATON_API_KEY out of logs and shared terminals, and use only trusted runtime environments. <br>
Risk: Create, update, transition, comment, connection-delete, and issue-delete actions can modify Jira state. <br>
Mitigation: Confirm the target issue, project, connection, and intended effect before allowing any write or delete action. <br>
Risk: Requests are proxied through Maton for managed OAuth access to Jira. <br>
Mitigation: Install this skill only if you trust Maton to proxy Jira OAuth access and have reviewed the Jira OAuth permissions. <br>


## Reference(s): <br>
- [ClawHub Jira Skill Page](https://clawhub.ai/byungkyu/skills/jira-api) <br>
- [Jira Cloud REST API v3 Introduction](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/) <br>
- [Jira Search Issues with JQL](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-jql-get) <br>
- [Jira Issues API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/) <br>
- [JQL Reference](https://support.atlassian.com/jira-service-management-cloud/docs/use-advanced-search-with-jira-query-language-jql/) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, and a Jira Cloud ID for Jira API calls.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
