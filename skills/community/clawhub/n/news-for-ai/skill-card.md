## Description:

Fetches real-time AI industry news, daily AI digests, and searches AI topics including products, models, and MCP services, then outputs structured JSON with clean text content and separated media resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sskun](https://clawhub.ai/user/sskun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, analysts, and content workflows use this skill to gather current AI news, daily digests, and targeted AI topic results for article writing or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependencies are not pinned to exact versions.

Mitigation: Install and run the skill in an isolated Python environment and review dependency resolution before operational use.

Risk: The skill contacts aibase.cn and returns Chinese-oriented AI news and search results.

Mitigation: Confirm that this source and network access are appropriate for the deployment, and validate returned content before using it in published analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sskun/skills/news-for-ai)
- [Data schemas](schemas.md)
- [AIBase news source](https://news.aibase.cn/news)
- [AIBase daily source](https://news.aibase.cn/daily)
- [AIBase search source](https://www.aibase.cn/search/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [JSON emitted to stdout, including Markdown-formatted article text and separated images, videos, and links when full content is fetched.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Errors are emitted to stderr with exit code 1; --no-content omits full article content and media fields for faster browsing.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
