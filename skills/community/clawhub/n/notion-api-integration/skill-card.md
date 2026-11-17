## Description:

Builds and debugs Notion API integrations for data sources, pages, blocks, properties, filters, files, webhooks, bulk imports, authentication, rate limits, pagination, and version migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to design, debug, and operate Notion API integrations from code, curl, or SDKs. It helps with access setup, schema-aware payloads, database and data-source queries, pagination, bulk imports and exports, sync workflows, file handling, comments, and common Notion API errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can access Notion pages connected to the user's integration token.

Mitigation: Use a least-privilege Notion integration and connect only the parent pages the workflow needs.

Risk: The skill keeps local operational notes under ~/Clawic/data.

Mitigation: Review local note contents and store only pointers to secrets, not token values or signed file URLs.

Risk: Write operations can alter, archive, or overwrite Notion content when the integration has write capabilities.

Mitigation: Keep write_mode at confirm-writes or dry-run for sensitive work and grant update, insert, comment, or user-email capabilities only when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/notion-api-integration)
- [Clawic Skill Page](https://clawic.com/skills/notion-api-integration)
- [Access, Integrations, and OAuth](auth.md)
- [Data Sources](data-sources.md)
- [Databases and Schemas](databases.md)
- [Pages](pages.md)
- [Blocks](blocks.md)
- [Property Values](properties.md)
- [Filters and Sorts](filters.md)
- [Pagination](pagination.md)
- [Bulk Work](bulk.md)
- [Sync](sync.md)
- [Files](files.md)
- [Search](search.md)
- [Users](users.md)
- [Comments](comments.md)
- [Errors, Retries, and Rate Limits](errors.md)
- [Working File Templates](memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, curl, and SDK-oriented code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Notion API requests, local note updates, migration runbooks, retry plans, and schema-aware payloads.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
