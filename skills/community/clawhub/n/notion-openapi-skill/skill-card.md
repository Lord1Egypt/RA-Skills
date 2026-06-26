## Description: <br>
Operate the Notion Public API through UXC with a curated OpenAPI schema for search, block traversal, page reads, content writes, and data source or database inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect, traverse, and update Notion workspace content through the Notion Public API when recursive reads or structured writes are needed beyond the Notion MCP surface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the caller's Notion API permissions to read or modify workspace content. <br>
Mitigation: Use a dedicated Notion integration connected only to the required pages, data sources, or databases. <br>
Risk: Create, update, append, trash, or delete operations can change Notion content. <br>
Mitigation: Confirm every write operation with the user before execution and grant write access only when required. <br>
Risk: A remote or changed OpenAPI schema could alter the available operation surface. <br>
Mitigation: Use a pinned or bundled schema for sensitive workflows. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/notion-public.openapi.json) <br>
- [Notion API reference](https://developers.notion.com/reference) <br>
- [Retrieve a database](https://developers.notion.com/reference/retrieve-a-database) <br>
- [Retrieve a block](https://developers.notion.com/reference/retrieve-a-block) <br>
- [Notion API versioning](https://developers.notion.com/reference/versioning) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Notion API JSON envelopes and requires caller review before write operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
