## Description:

Access and manage NocoDB databases via v3 REST API. Use for managing workspaces, bases, tables, fields, views, records, and more. Supports filtering, sorting, pagination, linked records, attachments, and team management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkmchinese](https://clawhub.ai/user/jkmchinese)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent inspect and manage NocoDB workspaces, bases, tables, fields, views, records, filters, sorts, attachments, scripts, teams, and API tokens through a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad database and administrative power over NocoDB resources.

Mitigation: Use a least-privilege NocoDB token and restrict the token to only the workspaces, bases, tables, and actions needed for the task.

Risk: Destructive commands can delete or alter workspaces, bases, tables, fields, views, records, filters, sorts, scripts, teams, or tokens.

Mitigation: List and confirm target IDs or names before running create, update, delete, member-management, script-management, team-management, token-management, or bulk record commands.

Risk: A misconfigured NOCODB_URL could send credentials and data to an unintended host.

Mitigation: Pin NOCODB_URL to a trusted HTTPS NocoDB host before use.

Risk: Attachment uploads, script changes, team changes, and token creation or deletion can have elevated operational impact.

Mitigation: Treat those commands as administrative actions and require explicit operator approval before execution.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jkmchinese/skills/nocodb-skills)
- [Default NocoDB service endpoint](https://app.nocodb.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and JSON command arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands produce JSON or tab-separated terminal output from NocoDB API responses.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
