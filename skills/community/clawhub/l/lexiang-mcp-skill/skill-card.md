## Description: <br>
Provides an agent with Lexiang knowledge-base capabilities for search, reading, document creation, block editing, file transfer, connector imports, and MCP setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lexiang](https://clawhub.ai/user/lexiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and knowledge-base administrators use this skill to connect an agent to a Lexiang workspace for document search, reading, authoring, block-level edits, file upload and download, connector imports, and workspace setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read from and write to a connected Lexiang workspace, including persistent document edits and file transfers. <br>
Mitigation: Install only when the agent should access the target Lexiang workspace; confirm the destination entry, local files, and network transfer before upload or folder sync. <br>
Risk: Bearer tokens and workspace credentials could expose sensitive knowledge-base access if mishandled. <br>
Mitigation: Store credentials carefully, use the documented OAuth or token renewal flow, and avoid placing secrets in folders selected for sync. <br>
Risk: Large folder or file operations can upload unintended content or exceed operational limits. <br>
Mitigation: Use dry-run planning and batch operations; the artifact directs batches of no more than 20 items and requires user notice for larger sets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lexiang/lexiang-mcp-skill) <br>
- [Lexiang platform](https://lexiangla.com) <br>
- [Lexiang MCP configuration](https://lexiangla.com/mcp) <br>
- [MCP protocol](https://modelcontextprotocol.io) <br>
- [Reference index](references/index.md) <br>
- [Setup and authentication](references/setup.md) <br>
- [Base data model and safety rules](references/base.md) <br>
- [Search and reading workflow](references/search.md) <br>
- [Writer workflow](references/writer.md) <br>
- [Block editing workflow](references/blocks.md) <br>
- [File transfer workflow](references/files.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, code snippets, MCP tool-call parameters, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate persistent Lexiang read, write, edit, delete, file-upload, and file-download actions through connected MCP tools; requires an OAuth or bearer-token connection.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
