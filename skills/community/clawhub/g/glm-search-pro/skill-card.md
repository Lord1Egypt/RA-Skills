## Description:

Zhipu GLM web search using cURL or MCP backends, with Pro, Sogou, Quark, and Std engines plus intent recognition, recency filtering, domain filtering, and configurable result detail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bithostgits](https://clawhub.ai/user/bithostgits)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when an agent needs current web search, news lookup, domain-scoped search, or online resource retrieval through Zhipu GLM search APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional MCP setup stores the Zhipu API key on disk and includes it in an MCP broker URL query parameter.

Mitigation: Use cURL mode when possible; if MCP mode is required, keep the generated mcporter config owner-only and avoid sharing logs or config files.

Risk: MCP setup or MCP use can invoke unpinned npm code through npx mcporter.

Mitigation: Review the MCP setup path before use, prefer cURL mode in untrusted environments, and pin or preinstall trusted mcporter tooling when operational policy requires it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bithostgits/skills/glm-search-pro)
- [Zhipu GLM Web Search API Reference](artifact/references/api-notes.md)
- [Zhipu Web Search Docs](https://docs.bigmodel.cn/cn/guide/tools/web-search)
- [Zhipu MCP Search Server Docs](https://docs.bigmodel.cn/cn/coding-plan/mcp/search-mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON search-result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include titles, summaries, links, source names, reference IDs, and optional publish dates.]

## Skill Version(s):

1.2.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
