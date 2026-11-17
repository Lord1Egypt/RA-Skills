## Description:

小红书全场景数据查询助手。支持App和Web多版本API，覆盖笔记详情、用户数据、搜索、商品、评论、话题等全功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Brands, marketers, and analysts can use this skill to query Xiaohongshu notes, users, products, comments, and topics, then summarize findings for content research, creator evaluation, and consumer trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags fallback instructions that may direct requests to a platform outside the stated Xiaohongshu scope.

Mitigation: Check that each endpoint matches the intended Xiaohongshu task and the documented service before making requests.

Risk: The scan is incomplete, with one component only partially examined.

Mitigation: Review the partially examined component and the flagged fallback guidance before installing or relying on the skill.

Risk: The skill sends the MaxHub API key to a third-party API service, and some endpoints may require platform session cookies.

Mitigation: Use a scoped API key and provide session cookies only when you trust the service; rotate or revoke cookies after use.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-xiaohongshu)
- [MaxHub API service and account setup](https://www.aconfig.cn)
- [ClawHub skill page](https://clawhub.ai/xiewxx/skills/maxhub-xiaohongshu-2)
- [Note API reference](artifact/references/api-note.md)
- [User API reference](artifact/references/api-user.md)
- [Search API reference](artifact/references/api-search.md)
- [Product and topic API reference](artifact/references/api-product-topic.md)
- [Parameter mappings](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown summaries and tables of Xiaohongshu API query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language; includes summaries for browse, analysis, and comparison requests.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
