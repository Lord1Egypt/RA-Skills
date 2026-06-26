## Description: <br>
Guides agents in using the mcp-local-rag MCP server to search the web with semantic similarity ranking across DuckDuckGo, Google, and multi-engine research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nkapila6](https://clawhub.ai/user/nkapila6) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to add web search and research workflows through a locally configured MCP server. It helps agents choose search backends, formulate queries, tune result counts, and cite source URLs when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may leave the local machine through whichever external search providers the configured server uses. <br>
Mitigation: Avoid secrets, credentials, and private personal data in search queries unless the backend configuration and logging behavior have been verified. <br>
Risk: The skill depends on a separate local RAG MCP server runtime. <br>
Mitigation: Install only after reviewing and approving the mcp-local-rag server dependency and its configured search backends. <br>
Risk: Search results can be incomplete, stale, or insufficient for important claims. <br>
Mitigation: Use multiple queries or backends for important facts and cite source URLs when they are available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nkapila6/local-rag-search) <br>
- [mcp-local-rag project](https://github.com/nkapila6/mcp-local-rag) <br>
- [mcp-local-rag README](https://github.com/nkapila6/mcp-local-rag#readme) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown prose with JSON configuration snippets and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a separately installed mcp-local-rag MCP server; search responses should include source URLs when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
