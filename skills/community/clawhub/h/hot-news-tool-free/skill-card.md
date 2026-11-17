## Description:

轻量级新闻聚合工具，自动搜索并筛选国内外科技、军事、社会新闻要点，帮助个人用户快速了解时事动态。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External personal users and news-focused agents use this skill to collect public news items across technology, military, and social categories, filter duplicate or low-quality items, and produce structured summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the release suspicious because command and write authority are broader than the stated news aggregation purpose.

Mitigation: Run the skill in a sandbox with restricted filesystem access and approve command execution only when it is directly tied to news aggregation.

Risk: The skill may install Python dependencies and contact third-party news websites during aggregation.

Mitigation: Review dependency installation commands, limit network access to expected news sources, and avoid providing credentials unless a trusted workflow requires them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/hot-news-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown news summaries with source labels, timestamps, links, and setup or execution commands where needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aggregates public news sources by category; the free version documents limits on scheduled updates, custom sources, real-time push notifications, and trend analysis.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
