## Description: <br>
Jira API integration with managed OAuth for searching issues with JQL, creating and updating issues, and managing projects and transitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to interact with Jira Cloud through Maton-managed OAuth, including issue search, issue creation and updates, project lookup, transitions, comments, and user queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive MATON_API_KEY and uses Maton-managed OAuth to access Jira data. <br>
Mitigation: Protect the API key, rotate it if exposed, and install the skill only when Maton is trusted to proxy Jira requests and manage OAuth. <br>
Risk: Requests can affect the wrong Jira workspace or connection when multiple Jira accounts are available. <br>
Mitigation: Select the intended cloud ID and specify the correct connection before making Jira API calls. <br>
Risk: Create, update, delete, transition, comment, or OAuth-connection deletion operations can modify Jira state. <br>
Mitigation: Require clear user confirmation of the target resource and intended effect before executing any write or deletion operation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/jira-api) <br>
- [Jira REST API v3 Introduction](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/) <br>
- [Jira Search Issues API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-jql-get) <br>
- [Jira Issues API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-get) <br>
- [JQL Reference](https://support.atlassian.com/jira-service-management-cloud/docs/use-advanced-search-with-jira-query-language-jql/) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, API calls, configuration] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, REST, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, Jira Cloud ID selection, and explicit confirmation before write operations.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
