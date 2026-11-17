## Description:

Create Jira tickets with web-researched content for Jira issues, tickets, stories, bugs, and tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cehd5170](https://clawhub.ai/user/cehd5170)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to create Jira tickets from user requests, optionally enriching the description with web research, acceptance criteria, reproduction steps, labels, priority, assignee, and components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Jira credentials can create or modify work items within the configured tenant and project permissions.

Mitigation: Use a Jira API token with the minimum project permissions needed for ticket creation and rotate it according to local credential policy.

Risk: Ticket descriptions may include confidential user input, internal details, or external research content.

Mitigation: Review the generated ticket content before creation, especially when the request includes sensitive context or web-researched material.

Risk: A misconfigured Jira base URL could send requests to the wrong Atlassian tenant.

Mitigation: Set JIRA_BASE_URL to the exact expected HTTPS Atlassian tenant before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cehd5170/skills/jira-ticket)
- [Atlassian API token setup](https://id.atlassian.com/manage-profile/security/api-tokens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown response with Jira issue key, direct URL, summary, research status, and cited sources when research is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates Jira issues through Jira REST API v3 using Atlassian Document Format descriptions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
