## Description:

Retrieve, analyze, and update Jira tickets through MCP-based or direct Jira REST API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to fetch Jira requirements, analyze acceptance criteria, search issues, and update ticket status or comments during delivery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and update Jira issues using the configured Jira account.

Mitigation: Use a dedicated Jira account or narrowly scoped token, and review proposed ticket changes before applying them.

Risk: Jira credentials could be exposed if hardcoded or stored in plain configuration files.

Mitigation: Use environment variables or a secrets manager, keep .env files out of source control, and rotate tokens if exposed.

Risk: The optional MCP package runs with Jira network access.

Mitigation: Pin or review the MCP package and run it with limited filesystem and network access.

## Reference(s):

- [Jira Ops ClawHub skill page](https://clawhub.ai/djc00p/skills/jira-ops)
- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration examples and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Jira MCP tool calls, REST API setup steps, ticket analysis summaries, comments, status transitions, and JQL searches.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
