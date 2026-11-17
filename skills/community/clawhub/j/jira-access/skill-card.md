## Description:

Access a Jira workspace (omeshkshatriya.atlassian.net) using provided email and API token to list, create, and transition issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brajesh9373](https://clawhub.ai/user/brajesh9373)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Jira workspace operators use this skill to list Jira issues with JQL, create issues, transition issues, and add comments through an agent-driven command workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live Jira data through create, transition, and comment commands.

Mitigation: Require explicit user approval before running commands that create issues, transition issues, or add comments.

Risk: The Jira API token is sent to the configured Jira domain, and the domain is not validated by the skill.

Mitigation: Set JIRA_DOMAIN only to the intended Atlassian tenant, use a least-privileged Jira API token, and rotate any token that may have run with an untrusted domain.

## Reference(s):

- [Jira REST API documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [ClawHub Jira Access skill page](https://clawhub.ai/brajesh9373/skills/jira-access)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JIRA_DOMAIN, JIRA_EMAIL, and JIRA_API_TOKEN environment variables; Jira write actions should require explicit user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
