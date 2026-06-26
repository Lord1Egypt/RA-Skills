## Description: <br>
AI 新闻聚合与热度排序工具，当用户询问 AI 领域最新动态时，收集新产品发布、研究论文、行业动态、融资新闻、开源项目更新、社区病毒传播现象和热门 AI 工具，并输出按热度排序、附原文链接的中文摘要列表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, analysts, and other users can use this skill to gather current AI news across newsletters, media, research sources, funding announcements, policy updates, and community discussions, then receive a concise Chinese digest sorted by estimated heat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs an agent to browse many public sources, which may be inappropriate for private intranet pages or sensitive internal sources. <br>
Mitigation: Use the skill only where broad public web browsing is acceptable and avoid directing it at private or sensitive internal sources. <br>
Risk: News aggregation can surface stale, duplicated, paywalled, or insufficiently corroborated items. <br>
Mitigation: Deduplicate same-event reports, prefer authoritative or detailed sources, mark paywalled content, and cross-check stories across source types before ranking them as high heat. <br>


## Reference(s): <br>
- [AI 新闻源推荐列表](references/sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/martin-ai-news-collector) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kirkraman) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown Chinese news digest with ranked sections and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected to summarize 15-25 deduplicated AI news items and include collection count, search count, covered dimensions, and update time.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
