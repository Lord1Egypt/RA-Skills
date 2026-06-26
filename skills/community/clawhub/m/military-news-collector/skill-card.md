## Description: <br>
军事新闻聚合与重要性排序工具。当用户询问军事领域最新动态时触发，如："今天有什么军事新闻？""最近有什么军事冲突？""全球军事局势如何？"。覆盖：地区冲突、武器装备、军事演习、国防政策、地缘政治、战争动态。输出中文摘要列表，按重要性排序，附带原文链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zgywayy](https://clawhub.ai/user/zgywayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to gather recent public military news, compare coverage across multiple source categories, and produce an importance-ranked Chinese summary with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public military and conflict news can be incomplete, stale, biased, or contradicted by later reporting. <br>
Mitigation: Verify important claims against the cited sources and prefer cross-confirmed factual reporting over opinion or single-source claims. <br>
Risk: The skill makes multiple public web searches and fetches news pages about military and conflict topics. <br>
Mitigation: Use only public sources, avoid private or restricted information, and review the final summary before relying on it. <br>


## Reference(s): <br>
- [Recommended Military News Sources](references/sources.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zgywayy/military-news-collector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown Chinese summary list with source links and importance ratings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 15-25 deduplicated news items, sorted by importance, with cited original links when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
