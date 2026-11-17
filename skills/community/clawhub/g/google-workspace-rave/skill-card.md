## Description:

Manage Google Workspace through the gws CLI for Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, Tasks, Meet, Slides, Forms, Contacts, and other Workspace APIs, returning structured JSON for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eladrave](https://clawhub.ai/user/eladrave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent inspect, create, update, share, send, and administer Google Workspace resources through the gws CLI. It is intended for Workspace automation tasks that need structured JSON responses and shell-command workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose or persist OAuth client secrets, callback URLs, tokens, and Workspace credentials.

Mitigation: Use least-privilege Google scopes, avoid pasting OAuth secrets or callback URLs into chat, keep credentials in a secret manager or protected file outside the workspace, and restrict credential file permissions.

Risk: Workspace operations can send email, share files, administer users, or delete data if executed without review.

Mitigation: Require explicit confirmation and dry-run previews before send, share, admin, delete, or other mutating actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eladrave/skills/google-workspace-rave)
- [Google Workspace CLI repository](https://github.com/googleworkspace/cli)
- [Google Workspace CLI skill recipes](https://github.com/googleworkspace/cli/tree/main/skills)
- [Google API Discovery Service](https://developers.google.com/discovery)
- [Advanced Usage](artifact/references/advanced.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with bash command examples and structured JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run previews, paginated NDJSON streams, selected response fields, and table output for human review.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
