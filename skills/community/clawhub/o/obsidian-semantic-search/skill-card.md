## Description:

Semantic search across your Obsidian vaults using local embeddings (Ollama + pgvector). 10 MCP tools: hybrid/semantic/keyword search, file CRUD, batch reads, live re-indexing, and a monitoring dashboard. Fully local, with no API keys, no cloud, and zero cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[celstnblacc](https://clawhub.ai/user/celstnblacc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Obsidian users use this skill to install and configure a local-first MCP server for semantic, keyword, and hybrid search across personal Obsidian vaults. It also supports vault file access, append or overwrite operations, re-indexing, and local monitoring once configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation path asks users to run remote shell scripts and to bypass a security warning.

Mitigation: Review the upstream repository and installer first, prefer a pinned release or commit with checksum or signature verification, and do not treat --force as evidence of safety.

Risk: The configured MCP server can index local vault contents and expose file read, append, overwrite, and re-indexing tools.

Mitigation: Use it only with vaults suitable for local indexing, and keep backups or version control before enabling write or overwrite workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/celstnblacc/skills/obsidian-semantic-search)
- [Publisher profile](https://clawhub.ai/user/celstnblacc)
- [Project homepage](https://github.com/celstnblacc/obsidian-semantic-mcp)
- [Architecture documentation](https://github.com/celstnblacc/obsidian-semantic-mcp/blob/main/docs/ARCHITECTURE.md)
- [Changelog](https://github.com/celstnblacc/obsidian-semantic-mcp/blob/main/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent toward local vault search, file reads, file writes, and re-indexing through the configured MCP server.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
