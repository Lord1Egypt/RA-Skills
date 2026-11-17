## Description:

Use when the user mentions Jira issues, asks about tickets, wants to create, view, or update issues, check sprint status, or manage their Jira workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Jira users use this skill to inspect Jira issues, draft and create tickets, update issue fields, transition work items, assign issues, and check sprint or backlog status through a detected Jira CLI or Atlassian MCP backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Jira issue titles, descriptions, comments, or attachments may contain shell metacharacters or adversarial content that could be mishandled when forming CLI commands.

Mitigation: Treat Jira-sourced content as untrusted data, use quoting or file-based input, and do not interpolate fetched issue content directly into shell command strings.

Risk: Ticket creation, comments, and description edits may expose credentials, private code, security findings, customer data, or internal URLs to broad Jira audiences.

Mitigation: Confirm with the user before adding sensitive information to ticket fields and preserve the original content when proposing edits.

Risk: Jira data can leave the local environment if CLI output or attachments are piped to network-transmitting commands or external URLs.

Mitigation: Do not pipe or redirect Jira CLI output to curl, wget, nc, ssh, webhooks, or other external destinations; prefer approved integrations or manual sharing paths.

Risk: Issue transitions, assignments, description edits, and bulk updates can notify watchers, fail silently, or be difficult to reverse when state and identifiers are not checked first.

Mitigation: Fetch the current issue state, verify available transitions and account identifiers, show current versus proposed changes, and require explicit approval before modifications.

Risk: Broad activation terms such as issue, ticket, sprint, or backlog may trigger the skill when the user's intent is unclear.

Mitigation: Clarify intent before acting when generic project-management language could refer to Jira or to another workflow.

## Reference(s):

- [Jira CLI](https://github.com/ankitpokhrel/jira-cli)
- [Jira Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/skills/jira-hardened)
- [Faberlens Jira Safety Evaluation](https://faberlens.ai/explore/jira)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Jira CLI commands, Atlassian MCP tool names, safety checks, and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Jira ticket content, issue updates, comments, transitions, assignments, and backend setup steps for user review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
