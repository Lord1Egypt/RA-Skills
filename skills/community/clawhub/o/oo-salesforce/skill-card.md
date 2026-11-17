## Description:

Salesforce (salesforce.com). Use this skill for ANY Salesforce request — reading, creating, updating, and deleting data. Whenever a task involves Salesforce, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to read and search Salesforce data and manage records, reports, files, Chatter, approvals, and email through an already connected OOMOL account. It guides the agent to inspect each action's schema first and to get confirmation before actions that change state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags automatic remote installation and undisclosed changes to other agent skills as warranting review.

Mitigation: Review and install a verified CLI release separately before enabling the skill; review persistent skill-management effects and use OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: Salesforce changes can affect records, emails, approvals, and deletions.

Mitigation: Use a narrowly permissioned Salesforce account and retain confirmation for changes, emails, approvals, and deletions.

## Reference(s):

- [Salesforce REST API documentation](https://developer.salesforce.com/docs/platform/api-rest/guide/intro-rest.html)
- [Salesforce](https://www.salesforce.com)
- [oo CLI commands and environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Salesforce skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-salesforce)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured Salesforce action results and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may contain Salesforce record data or action outcomes.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
