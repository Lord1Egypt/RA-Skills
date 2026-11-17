## Description:

按关键词搜索抖音公开视频与图文、用户、作品、评论和实时热榜，并提供结构化数据供选题、竞品研究和公域获客分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

面向内容运营、增长和数据分析人员，用于查找公开内容与账号、分析评论需求、跟踪热点，并整理竞品情报或潜在线索。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin links or IDs are sent to a third-party API; the security review notes disclosure may be unclear.

Mitigation: Send only public, non-sensitive query terms and IDs, and confirm you are comfortable with the third-party processing before use.

Risk: Comment results can include public user identifiers that could be misused in outreach or shared datasets.

Mitigation: Limit follow-up to authorized internal use, avoid harassment or resale, and remove identifiers before sharing results externally.

## Reference(s):

- [GuaiKei API service and token information](https://www.guaikei.com)
- [Customer acquisition workflow](references/customer-acquisition.md)
- [Demand mining guide](references/demand-mining.md)
- [Command options](references/options.md)
- [Output contract](references/contract.md)
- [Error handling](references/errors.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown, Guidance]

**Output Format:** [Structured JSON results with optional Markdown summaries and tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selected queries save JSON logs; available fields depend on the public data returned.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
