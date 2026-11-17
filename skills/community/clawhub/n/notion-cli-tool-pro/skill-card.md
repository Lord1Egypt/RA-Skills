## Description:

Notion命令行(专业版) helps agents operate Notion through CLI-oriented workflows for multi-workspace management, file upload, schema changes, page movement, batch operations, custom output, and audit logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation engineers, and teams use this skill to let an agent prepare and run Notion CLI commands for querying, modifying, exporting, syncing, and auditing Notion workspace content at team or enterprise scale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to run Notion CLI commands with broad read, write, move, delete, export, and sync access to workspace data.

Mitigation: Use least-privilege Notion tokens, avoid broad workspace keys, and review every write, delete, export, or sync command before execution.

Risk: The skill describes integrations with external destinations such as warehouses, webhooks, S3-compatible storage, scheduled jobs, and Redis caching.

Mitigation: Enable those features only after verifying the destination, access controls, retention settings, and operational need.

Risk: Batch operations and schema changes can modify or remove large amounts of Notion data.

Mitigation: Use dry-run previews, checkpoints, idempotency keys, and backups before applying large write or delete operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/notion-cli-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and JSON-shaped command results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include commands that read, modify, delete, export, or sync Notion workspace data and should be reviewed before execution.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version and artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
