## Description:

Read, search, export, create, update, monitor, query, inspect, batch-edit, and explicitly archive Notion pages and databases. Use when the user requests Notion content or database operations and a host secret manager can supply NOTION_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robansuini](https://clawhub.ai/user/robansuini)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to synchronize Markdown and Notion content, search and query Notion workspaces, inspect schemas, monitor page changes, and perform controlled page or database updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Notion integration token can expose any Notion pages and databases shared with that integration.

Mitigation: Use a least-privilege Notion integration, share only required pages or databases, and store NOTION_API_KEY only in a secret manager.

Risk: Batch updates or archive operations can modify Notion content at scale.

Mitigation: Prefer dry runs before batch updates, review database filters carefully, and rely on the explicit archive confirmation flow for page archiving.

Risk: Monitoring can create ongoing access to Notion page state and local watch-state files.

Mitigation: Enable scheduled monitoring only when ongoing checks are intended and keep watch-state files within authorized workspace paths.

## Reference(s):

- [Notion Sync API Reference](references/API-REFERENCE.md)
- [Migrating notion-sync from v1/v2 to v3](references/MIGRATION-V3.md)
- [ClawHub Skill Page](https://clawhub.ai/robansuini/skills/notion-sync)
- [Notion API Host](https://api.notion.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON script output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts can read or write selected Markdown and watch-state files, call the Notion API, and emit machine-readable JSON when --json is used.]

## Skill Version(s):

3.0.2 (source: server release evidence and changelog, released 2026-09-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
