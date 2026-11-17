## Description:

Jira (atlassian.com). Use this skill for ANY Jira request — reading, creating, and updating data. Whenever a task involves Jira, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Jira users can use the skill to find projects, search and read issues and comments, create issues, and add comments through their connected Jira account. It requires the oo CLI and a connected Jira account; changes to Jira require user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run a remote CLI installer without a separate approval step, and the installer's behavior was not verified.

Mitigation: Review the installer separately and use a verified, fixed release before setup; grant only the Jira permissions needed.

## Reference(s):

- [Jira](https://www.atlassian.com/software/jira)
- [Jira Cloud REST API documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector requests and responses, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read and search actions return Jira data; write actions require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
