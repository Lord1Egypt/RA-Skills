## Description:

掘金工具帮助个人用户查询掘金热门内容、下载文章为 Markdown，并以登录会话创建 Markdown 草稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

个人用户和开发者在明确的掘金任务中使用该技能查询热门文章、下载单篇或少量作者文章，并将本地 Markdown 创建为掘金草稿。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad or contradictory activation instructions could cause the skill to be invoked for unrelated database, SQL, ETL, or general automation tasks.

Mitigation: Enable and use the skill only for explicit Juejin tasks, and correct trigger text before broader deployment.

Risk: The skill carries command, file, login-cookie, and publishing capabilities.

Mitigation: Review before installing, run only in trusted environments, require explicit paths for file operations, and keep publishing in draft mode unless the user provides the required confirmation.

Risk: Login-based publishing stores a Juejin session cookie at $HOME/.juejin_cookie.json.

Mitigation: Treat the cookie as sensitive session data, avoid shared or CI environments, keep file permissions restricted, and remove the cookie after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/juejin-tool-free)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)
- [Juejin category briefs API](https://api.juejin.cn/tag_api/v1/query_category_briefs)
- [Juejin category feed API](https://api.juejin.cn/recommend_api/v1/article/recommend_cate_feed)
- [Juejin all feed API](https://api.juejin.cn/recommend_api/v1/article/recommend_all_feed)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, plain text status messages, draft links, and command/API call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloaded articles are saved under ./output/; publishing workflows default to draft creation and may use a local Juejin session cookie.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
