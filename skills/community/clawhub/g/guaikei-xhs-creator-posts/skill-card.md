## Description:

根据小红书链接类型自动路由：笔记链接(explore/)走详情或评论、博主主页(user/profile/)走作品列表、短链(xhslink)按目标解析。当用户给出小红书链接并想了解其内容时使用本技能；即使用户没说"分析"，只要粘贴了链接并询问相关内容也适用。不用于非小红书链接或需登录的页面。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External content creators, marketers, data analysts, and account operators use this skill to query public Xiaohongshu content, retrieve note details and comments, and monitor creator posts for content research, competitor monitoring, KOL screening, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords or URLs and the GUAIKEI_API_TOKEN to www.guaikei.com.

Mitigation: Install and run it only when that data transfer is acceptable; treat the token like a password and rotate it if exposed.

Risk: Fetched content, research history, and access-bearing Xiaohongshu URLs can be retained in generated logs.

Mitigation: Review the generated logs/ directory after use and delete files that should not be retained or shared.

Risk: The skill is intended for public Xiaohongshu data and does not support private, hidden, or login-only content.

Mitigation: Use it only with public Xiaohongshu keywords, note links, or creator profile links, and do not use results for prohibited redistribution or unlawful purposes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-creator-posts)
- [Guaikei API token and support site](https://www.guaikei.com)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Analysis, Guidance]

**Output Format:** [JSON status envelopes with optional Markdown summaries and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; successful CLI runs save fetched results under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
