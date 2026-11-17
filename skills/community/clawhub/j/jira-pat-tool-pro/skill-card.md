## Description:

Jira PAT 管理专业版 helps agents manage Jira issues with PAT-based access, JQL search, batch operations, workflow automation, and audit-oriented change tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and automation users can use this skill to inspect Jira issues, run JQL searches, perform controlled batch issue operations, and prepare workflow or audit outputs through an agent. It is intended for Jira environments where users can provide scoped credentials and review changes before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Jira operations could affect real projects if the agent is granted broad credentials or unsupervised authority.

Mitigation: Use least-privilege Jira tokens, pin JIRA_URL to a trusted Jira host, and require explicit confirmation before bulk creation, workflow transitions, field or component changes, webhook use, or CI/CD-triggered issue closure.

Risk: Broad environment-variable checks may expose unrelated secret names or values during setup and troubleshooting.

Mitigation: Avoid broad environment scans in shared environments and redact credential values from all agent-visible output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jira-pat-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Jira operation summaries, execution logs, configuration examples, and structured status or error data.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
