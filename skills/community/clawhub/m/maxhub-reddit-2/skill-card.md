## Description:

Reddit 数据查询助手。覆盖帖子详情、版块、用户、搜索、评论、推荐等全功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and researchers use the skill to retrieve and summarize Reddit posts, subreddit information, user activity, search results, and comments for community monitoring, trend research, and content discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented npx clawhub install command is unpinned, so installer code could change before a future install.

Mitigation: Review the release and installer source before installing; pin or verify a specific release when the installer supports it.

Risk: Security review coverage is partial because two references in SKILL.md could not be resolved and their targets were not assessed.

Mitigation: Review the unresolved reference targets before relying on them.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/XieWxx/maxhub-reddit)
- [MaxHub API and account setup](https://www.aconfig.cn)
- [Post API reference](references/api-post.md)
- [Subreddit API reference](references/api-subreddit.md)
- [User and search API reference](references/api-user-search.md)
- [Parameter mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Configuration instructions]

**Output Format:** [Markdown summaries, lists, and comparison tables with optional inline setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses summarize data returned by the MaxHub API; conclusions depend on the available API results.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata; packaged skill frontmatter reports 3.6.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
