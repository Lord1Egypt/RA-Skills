## Description:

知乎数据查询助手。覆盖用户信息、搜索、专栏、问答、热榜、评论等全功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to retrieve and summarize Zhihu user profiles, search results, articles, questions, comments, and trending topics for research, content planning, and discussion monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates this release suspicious with medium confidence and says its analysis is partial because two references were unresolved; it specifically calls out Douyin fallback and broad activation examples.

Mitigation: Review the documented Douyin fallback and broad activation examples against the intended use before installing or enabling the skill.

Risk: The security guidance notes an unpinned installation command.

Mitigation: Use an installation command pinned to a release version you have reviewed.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/XieWxx/maxhub-zhihu)
- [MaxHub API service](https://www.aconfig.cn)
- [User Data API reference](references/api-user.md)
- [Search & Trending API reference](references/api-search-trending.md)
- [Content API reference](references/api-content.md)
- [Parameter Mappings reference](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Bilingual Chinese or English Markdown summaries, lists, and comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Language follows the user; results are based on API responses.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
