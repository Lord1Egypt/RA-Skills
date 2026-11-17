## Description:

Builds a runnable MCP knowledge server from a website or documentation URL by crawling pages, extracting concepts, building a knowledge graph, generating embeddings, and producing installable server files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nacmonad](https://clawhub.ai/user/nacmonad)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to turn public documentation, tutorials, or learning sites into searchable MCP knowledge servers for Claude Desktop or compatible agent environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can crawl arbitrary URLs and preserve untrusted web content in generated knowledge bases.

Mitigation: Run it only against public documentation you trust, and avoid authenticated, internal, or sensitive URLs.

Risk: The scripts can automatically install Python packages or browser dependencies.

Mitigation: Use an isolated virtual environment or container, pin and review dependencies, and disable automatic package installation on sensitive machines.

Risk: The generated server.py and mcp_config.json become part of the Claude Desktop tool surface.

Mitigation: Review generated server.py and mcp_config.json before adding them to Claude Desktop.

## Reference(s):

- [GraphRAGBuilder ClawHub skill page](https://clawhub.ai/nacmonad/skills/graph-rag-builder)
- [Publisher profile](https://clawhub.ai/user/nacmonad)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Strudel workshop example target](https://strudel.cc/workshop/getting-started/)
- [Anthropic Skills announcement](https://www.anthropic.com/news/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus generated Python and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an output folder containing crawled content, extracted concepts, graph JSON, numpy embedding indexes, server.py, and mcp_config.json.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
