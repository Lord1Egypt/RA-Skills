## Description: <br>
Semantic search across your Obsidian vaults using local embeddings with Ollama and pgvector, including hybrid, semantic, and keyword search, file operations, live re-indexing, and a monitoring dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[celstnblacc](https://clawhub.ai/user/celstnblacc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Obsidian users use this skill to install and configure a local MCP server that lets an assistant search, read, append to, overwrite, and re-index notes in a selected vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer guidance includes unpinned remote scripts and upstream setup commands. <br>
Mitigation: Review and pin the upstream installer before running it, and avoid force-installing solely because the skill suggests it. <br>
Risk: The connected MCP server and assistant can search, read, append to, and overwrite files in the selected Obsidian vault. <br>
Mitigation: Back up the vault, restrict OBSIDIAN_VAULT to notes you are willing to expose, and review assistant-initiated writes. <br>
Risk: Remote Ollama mode may expose vault-derived content to another host. <br>
Mitigation: Use fully local mode unless the remote Ollama host is trusted and access controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/celstnblacc/obsidian-semantic-search) <br>
- [Project homepage](https://github.com/celstnblacc/obsidian-semantic-mcp) <br>
- [Architecture documentation](https://github.com/celstnblacc/obsidian-semantic-mcp/blob/main/docs/ARCHITECTURE.md) <br>
- [Changelog](https://github.com/celstnblacc/obsidian-semantic-mcp/blob/main/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local vault search and file operations through the configured MCP server.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
