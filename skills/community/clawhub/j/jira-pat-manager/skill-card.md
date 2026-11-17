## Description:

Jira PAT管理器 helps agents manage Jira personal access tokens through supervised token creation, revocation, permission configuration, and API-style responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, Jira administrators, and automation operators use this skill for supervised Jira personal access token management tasks, including creating, revoking, and adjusting permissions for tokens. It is best suited to explicit PAT-management requests where each state-changing action can be reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-management actions can create, revoke, or alter Jira access.

Mitigation: Use the skill only for explicit PAT-management tasks and require review before any state-changing action is executed.

Risk: The skill requests broad local read, write, and execution capabilities while its invocation boundaries are unclear.

Mitigation: Run it in a supervised environment with least-privilege credentials and confirm proposed commands, file writes, and API calls before execution.

Risk: Credential material such as API keys or PATs may be exposed if copied into prompts, logs, or output files.

Mitigation: Provide secrets through environment variables or the agent platform's secret store, avoid hardcoding tokens, and redact credential values from outputs and logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jira-pat-manager)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-style responses with optional shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credential-handling guidance, API request or response structures, troubleshooting steps, and supervised state-changing Jira PAT operations.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
