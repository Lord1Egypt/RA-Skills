## Description:

OpenProject CRUD skill for managing work packages, projects, groups, news, users, watchers, relations, notifications, time entries, comments, attachments, wiki pages, statuses, and related OpenProject API v3 resources with API token authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdelkrim](https://clawhub.ai/user/abdelkrim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and automation agents use this skill to inspect and update OpenProject work tracking, collaboration, notification, attachment, and time-entry data across cloud or self-hosted OpenProject instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A powerful OpenProject API token can expose or change project, user, group, notification, attachment, news, and workflow data according to the token holder's permissions.

Mitigation: Use a dedicated least-privilege OpenProject account and token, avoid admin tokens unless required, and review high-impact commands before allowing an agent to run them.

Risk: If OP_HOST is configured with an HTTP URL, the API token can be sent over an unencrypted connection.

Mitigation: Use HTTPS-only OP_HOST values and reject plaintext OpenProject endpoints in deployment configuration.

Risk: Bulk notification, custom action, group or user management, news, delete, and attachment-upload commands can create visible or destructive changes.

Mitigation: Require human review for broad or destructive operations and keep the skill's explicit confirmation requirements enabled for delete commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abdelkrim/skills/openproject-by-altf1be)
- [OpenProject API v3 coverage and limitations](docs/API-COVERAGE.md)
- [OpenProject](https://www.openproject.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and concise command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OP_HOST and OP_API_TOKEN environment variables; optional OP_DEFAULT_PROJECT, OP_MAX_RESULTS, and OP_MAX_FILE_SIZE tune default behavior.]

## Skill Version(s):

2.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
