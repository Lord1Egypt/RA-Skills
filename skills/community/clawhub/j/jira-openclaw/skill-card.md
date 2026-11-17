## Description:

Connect OpenClaw to Jira Cloud with secret-safe API access via pastewatch redaction. Includes credential setup, REST API helper script, JQL patterns, focus auto-linker cron, and overdue ticket bumper. Use when integrating Jira into an OpenClaw agent, setting up Jira cron jobs, or querying issues from chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppiankov](https://clawhub.ai/user/ppiankov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect an OpenClaw agent to Jira Cloud, configure credential handling, issue queries, Jira REST calls, and scheduled Jira workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent reusable authenticated Jira API access.

Mitigation: Use a least-privileged Jira token, restrict access to specific projects, and add endpoint and method allowlists before allowing calls to jira.sh.

Risk: Scheduled workflows can mutate Jira issues, including due dates and links.

Mitigation: Require explicit approval for automated mutations and review cron behavior before enabling write operations.

Risk: Credentials are stored in a sourced shell environment file.

Mitigation: Keep the secret file permission-restricted, use pastewatch redaction as described, and prefer a dedicated secret manager when available.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ppiankov/skills/jira-openclaw)
- [Agent-Native CLI Convention](https://ancc.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash code blocks, JQL examples, and JSON request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pastewatch-cli with an MCP server, curl, and python3; examples assume Jira Cloud REST API access.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
