## Description: <br>
Search local documents, files, notes, and knowledge bases. Index directories, search with BM25/vector/hybrid, get AI answers with citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicoataiza](https://clawhub.ai/user/nicoataiza) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and knowledge workers use this skill to index local folders, search files and notes with keyword, vector, or hybrid retrieval, and ask grounded questions over local documents. It also helps configure a local web UI or MCP integration for document access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexing broad or sensitive folders can make private documents searchable by the local tool or connected clients. <br>
Mitigation: Index only intended folders and avoid secrets, credentials, and broad home-directory collections. <br>
Risk: Serving a web UI for private documents can expose indexed content if bound too broadly. <br>
Mitigation: Bind the web UI to localhost when handling private documents. <br>
Risk: MCP write tools and administrative commands can make persistent local changes. <br>
Mitigation: Enable MCP write tools and run reset, cleanup, or skill-install commands only when those changes are explicitly desired. <br>


## Reference(s): <br>
- [GNO CLI Reference](cli-reference.md) <br>
- [GNO Usage Examples](examples.md) <br>
- [GNO MCP Installation](mcp-reference.md) <br>
- [GNO MCP Documentation](https://www.gno.sh/docs/MCP) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented command examples when the user asks for scripting or machine-readable output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
