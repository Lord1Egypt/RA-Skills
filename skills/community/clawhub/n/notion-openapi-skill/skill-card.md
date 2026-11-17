## Description:

Operate the Notion Public API through UXC with a curated OpenAPI schema for search, block traversal, page reads, content writes, and data source/database inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search, traverse, inspect, and update Notion workspace content through REST API operations exposed by UXC. It is especially useful when recursive block traversal or structured writes are needed beyond a standard Notion MCP workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Notion integration token can grant broad read or write access to connected workspace content.

Mitigation: Use a dedicated Notion integration token stored in an environment variable or secret store, and connect it only to the specific pages, data sources, or databases intended for agent access.

Risk: Write, trash, and delete operations can change or remove Notion content.

Mitigation: Require explicit user confirmation and a clear change summary before page creation, page updates, block appends, block updates, trash, or delete operations.

Risk: Reusing the notion-mcp credential can create cross-tool authentication side effects.

Mitigation: Prefer a separate notion-openapi credential; use the shared credential path only after accepting the interoperability tradeoff and validating the effective auth binding.

Risk: Fetching a mutable OpenAPI schema URL can change the linked API surface over time.

Mitigation: Pin or review the OpenAPI schema before linking the CLI for operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/notion-openapi-skill)
- [Usage Patterns](references/usage-patterns.md)
- [Curated Notion Public API OpenAPI Schema](references/notion-public.openapi.json)
- [Notion API Reference](https://developers.notion.com/reference)
- [Notion API Versioning](https://developers.notion.com/reference/versioning)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces UXC command guidance for Notion REST API calls; API responses are expected as JSON from the linked CLI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
