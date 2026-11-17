## Description:

Provides Jira Cloud REST API v3 guidance for managing issues, sprints, boards, epics, projects, users, and related DevOps data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffersonling1217-png](https://clawhub.ai/user/jeffersonling1217-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Jira operators use this skill to automate Jira Cloud work, including issue management, JQL searches, sprint and board operations, project lookup, user lookup, and Jira API request construction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable an agent to read and modify Jira data with the user's Atlassian token.

Mitigation: Use a least-privilege Jira account or token and limit project permissions to the required work.

Risk: Delete, bulk create, notification, sprint, board, and issue-changing actions can have broad workspace impact.

Mitigation: Require human review before executing destructive, bulk, notification, or workflow-changing requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffersonling1217-png/skills/jira-atlassian)
- [ClawHub metadata homepage](https://clawhub.ai/jeffersonling1217-png/jira-atlassian)
- [Atlassian API token management](https://id.atlassian.com/manage-profile/security/api-tokens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with REST endpoint examples, JSON request bodies, and environment variable guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JIRA_EMAIL, JIRA_API_TOKEN, and JIRA_DOMAIN for Jira Cloud actions.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
