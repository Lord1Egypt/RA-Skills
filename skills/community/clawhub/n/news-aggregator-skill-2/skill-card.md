## Description:

Comprehensive news aggregator that fetches, filters, and deeply analyzes real-time content from 8 major sources: Hacker News, GitHub Trending, Product Hunt, 36Kr, Tencent News, WallStreetCN, V2EX, and Weibo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonyliu9189](https://clawhub.ai/user/tonyliu9189)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to gather multi-source news, filter by broad or targeted topics, and produce concise Chinese-language news briefings with deeper interpretation of important items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to news and social sources and may store generated reports locally.

Mitigation: Review whether the topics and retained reports are appropriate for the environment before using the skill on shared machines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tonyliu9189/skills/news-aggregator-skill-2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown report in chat and timestamped Markdown file; fetch results are JSON when using the news-fetching script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved under reports/; deep mode can include extracted article text.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
