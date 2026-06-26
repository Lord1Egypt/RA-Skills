## Description: <br>
Reflective Memory gives agents a persistent semantic memory layer for storing, searching, retrieving, and reflecting on notes, files, URLs, commitments, and working context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hughpyle](https://clawhub.ai/user/hughpyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Reflective Memory to add durable memory, semantic search, document indexing, and reflection workflows to coding agents and MCP-compatible tools. It is suited for agents that need to remember prior work, surface relevant context, track commitments, and capture learnings across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change agent integrations and workspace-local agent configuration. <br>
Mitigation: Review the intended agent integrations and generated workspace configuration before enabling the skill in shared or sensitive workspaces. <br>
Risk: The skill can automatically capture sessions and index workspace files, which may include private source, customer data, or secrets. <br>
Mitigation: Configure indexing paths and excludes before use, and avoid broad workspace indexing where sensitive content is present. <br>
Risk: Summarization or embedding providers may process indexed content outside the local machine when external providers are configured. <br>
Mitigation: Use local providers or disable broad indexing when content should not be sent to external services. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hughpyle/keep) <br>
- [PyPI package](https://pypi.org/project/keep-skill/) <br>
- [Hosted service](https://keepnotes.ai) <br>
- [Quick Start](docs/QUICKSTART.md) <br>
- [MCP integration](docs/KEEP-MCP.md) <br>
- [OpenClaw integration](docs/OPENCLAW-INTEGRATION.md) <br>
- [Python API reference](docs/PYTHON-API.md) <br>
- [Agent guide](docs/AGENT-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI/MCP text responses with optional YAML frontmatter and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MCP responses can be token-budgeted; CLI output includes IDs, summaries, tags, related items, and version history.] <br>

## Skill Version(s): <br>
0.109.0 (source: frontmatter, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
