## Description:

Create, read, update, and delete documents, spreadsheets, and slide presentations in Mila via the REST API or MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freddyjd](https://clawhub.ai/user/freddyjd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage Mila collaborative documents, workbooks, slide decks, and server-organized content through documented REST endpoints or MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access documents, sheets, slide content, and server metadata available to the configured Mila API key.

Mitigation: Install only when Mila is trusted with that content and use the narrowest available API scopes.

Risk: Broad team API keys in MCP configuration can expose more collaborative content than the immediate task requires.

Mitigation: Prefer individual or narrowly scoped keys and avoid placing broad team keys into shared MCP configs.

Risk: Delete operations and full-content replacement can permanently remove or overwrite collaborative content.

Mitigation: Require explicit confirmation before delete or full replacement operations, and verify resource IDs before execution.

## Reference(s):

- [Mila homepage](https://mila.gg)
- [Mila API documentation](https://mila.gg/docs)
- [Mila MCP integration guide](https://mila.gg/mcp)
- [Documents reference](references/DOCUMENTS.md)
- [Sheets reference](references/SHEETS.md)
- [Slides reference](references/SLIDES.md)
- [Servers reference](references/SERVERS.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include REST request examples, MCP tool names, and resource identifiers supplied by the user.]

## Skill Version(s):

1.0.2 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
