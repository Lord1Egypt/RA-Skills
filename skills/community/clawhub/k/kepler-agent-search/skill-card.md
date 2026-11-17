## Description:

Kepler Agent Search helps an AI agent search and read content across web, social, code, academic, data, finance, and recruiting sources through the Kepler MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mylike2018](https://clawhub.ai/user/mylike2018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route searches across Bing, Baidu, Zhihu, Xiaohongshu, GitHub, arXiv, 199it, Eastmoney, Zhaopin, and 51job, then read selected results for research, comparison, and summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, URLs, and page-reading requests are routed through the Kepler MCP service and third-party sources.

Mitigation: Use the skill only when external search is intended, and avoid secrets, regulated data, private prompts, or internal-only information.

Risk: The skill requires a Kepler API key in MCP configuration.

Mitigation: Keep the API key out of committed project files and prefer user-scoped or secret-managed configuration.

Risk: Search results and external pages can be stale, incomplete, gated, subjective, or unreliable.

Mitigation: Cross-check important claims across sources and review source quality before relying on findings.

## Reference(s):

- [Kepler Agent Search ClawHub page](https://clawhub.ai/mylike2018/skills/kepler-agent-search)
- [Kepler MCP service endpoint](https://apisec.cn/sse)
- [Kepler MCP setup guide](references/mcp-setup.md)
- [Web search reference](references/search.md)
- [Social search reference](references/social.md)
- [GitHub search reference](references/github.md)
- [arXiv search reference](references/arxiv.md)
- [Industry data reference](references/data.md)
- [Finance search reference](references/finance.md)
- [Career search reference](references/career.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown and text with inline tool parameters and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include search result summaries, extracted page content, multi-source comparison reports, and MCP setup guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
