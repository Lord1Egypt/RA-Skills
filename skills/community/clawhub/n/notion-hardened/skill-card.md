## Description:

Notion API for creating and managing pages, databases, and blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to work with Notion pages, data sources, databases, and blocks through documented API calls while applying workspace access and data-handling guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A powerful Notion workspace credential can expose pages, databases, or shared workspace content beyond the user's intent.

Mitigation: Use a least-privilege Notion integration shared only with the pages and databases needed for the task.

Risk: API key examples and local token files can lead to credential exposure if secrets are pasted into chat or stored with weak file permissions.

Mitigation: Avoid pasting API keys into chat, prefer a secret manager or protected environment variable, set owner-only permissions on any local token file, and rotate the token if exposure is possible.

Risk: Broad search or read operations can reveal personal or sensitive Notion content the user did not explicitly request.

Mitigation: Access only pages and databases the user explicitly identifies by name, URL, or ID.

Risk: Bulk, destructive, or schema-changing Notion operations can cause data loss across shared workspaces.

Mitigation: Show affected page titles or record counts and require user confirmation before archiving, deleting, modifying schemas, or creating more than five items.

## Reference(s):

- [Notion Developers](https://developers.notion.com)
- [Notion Integrations](https://notion.so/my-integrations)
- [ClawHub Skill Release](https://clawhub.ai/snazar-faberlens/skills/notion-hardened)
- [Faberlens Notion Safety Evidence](https://faberlens.ai/explore/notion)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses NOTION_API_KEY and produces guidance and commands for Notion API operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
