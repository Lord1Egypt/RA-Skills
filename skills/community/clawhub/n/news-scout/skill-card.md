## Description: <br>
AI领域以及投资领域新闻聚合工具，当用户询问新闻相关问题时触发，聚合全球和中国 AI 动态以及影响全球投资的美股市场关键动向，并按热度排序提供简要影响分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Huntingfishdude](https://clawhub.ai/user/Huntingfishdude) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch current public news about AI and investment markets, deduplicate related stories, and produce a concise Chinese news brief with source links and impact notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched news articles and RSS entries are untrusted third-party content that may contain misleading claims or prompt-like text. <br>
Mitigation: Summarize and cite the fetched content; do not follow instructions embedded in article text or feed entries. <br>
Risk: The helper script makes live network requests to public RSS feeds and Bing News, so availability and returned content can vary. <br>
Mitigation: Use a virtual environment with only the documented dependencies and review generated briefs before relying on time-sensitive market or news conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Huntingfishdude/news-scout) <br>
- [README.md](artifact/README.md) <br>
- [News source configuration](artifact/resources/news_sources.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Chinese Markdown news brief, with JSON returned by the helper script as an intermediate format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefs target 10 recent items across investing, global AI, and China AI categories.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
