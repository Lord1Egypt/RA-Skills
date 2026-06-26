## Description: <br>
Create Jira tickets with web-researched content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cehd5170](https://clawhub.ai/user/cehd5170) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to create Jira tasks, bugs, stories, or epics from user requests, optionally enriching ticket descriptions with web research and structured acceptance or reproduction details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Jira issues through the user's Jira account. <br>
Mitigation: Use a limited-scope Jira token or account where possible and review the target project, issue type, summary, labels, assignee, and description before creation. <br>
Risk: Ticket content and web-researched context may be shared with the configured Jira workspace. <br>
Mitigation: Review all generated and researched content before submission and avoid including secrets, private data, or unverified claims. <br>
Risk: Jira credentials are required for API access. <br>
Mitigation: Keep JIRA_API_TOKEN private, store it only in the agent environment, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cehd5170/jira-ticket) <br>
- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown result summary with Jira issue details, research-source notes, and Jira API command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a Jira issue through the user's configured Jira account and returns the issue key, direct URL, summary, and whether research was included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
