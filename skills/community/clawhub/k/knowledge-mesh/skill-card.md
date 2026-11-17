## Description:

Knowledge Mesh is a cross-platform knowledge search agent for unified search, ranking, deduplication, monitoring, local indexing, Obsidian note search, and report export across supported knowledge sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjing5024064](https://clawhub.ai/user/hanjing5024064)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support engineers, and knowledge workers use this skill to find and organize technical or team knowledge across public APIs, workspace tools, local files, and Obsidian notes. It helps agents return structured search results, synthesize findings, monitor topics, and export reports while respecting configured source access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles work tokens, local note contents, search history, and file exports with weak scoping or safety controls.

Mitigation: Review before installing in a work environment; use narrowly scoped read-only service tokens and protect or clear KM_DATA_DIR when it may contain sensitive history or indexed metadata.

Risk: Searches and exported reports can expose confidential queries, incident details, workspace content, or local note metadata.

Mitigation: Avoid searching for secrets or confidential incident text unless local logging is acceptable, and export reports only to explicitly chosen safe paths.

Risk: A configured Confluence URL could direct requests to an untrusted host.

Mitigation: Set KM_CONFLUENCE_URL only to a trusted HTTPS Confluence host.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hanjing5024064/skills/knowledge-mesh)
- [Knowledge Mesh README](assets/README.md)
- [API 端点参考](references/api-endpoints.md)
- [搜索语法指南](references/search-syntax.md)
- [GitHub REST Search API](https://docs.github.com/en/rest/search)
- [Stack Exchange API Docs](https://api.stackexchange.com/docs)
- [Discord Developer Docs](https://discord.com/developers/docs)
- [Confluence Cloud REST API](https://developer.atlassian.com/cloud/confluence/rest/)
- [Notion API Reference](https://developers.notion.com/reference)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, JSON command output, shell command snippets, Markdown reports, and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read configured API tokens and local knowledge paths from environment variables; may write local index, monitoring, history, Markdown, and CSV files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
