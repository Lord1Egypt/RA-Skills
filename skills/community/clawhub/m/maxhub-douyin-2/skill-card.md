## Description:

抖音数据查询与工具助手。覆盖视频详情、用户数据、搜索、热榜、创作者工具、星图达人、内容指数等模块。含部分交互触发和协议工具接口（已标注）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, creator agencies, and content operations teams use the skill to query Douyin trends, assess creator performance, and monitor content and audience metrics. A MaxHub API key is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes an unpinned installer and incomplete scan coverage.

Mitigation: Review the installer source and pin a trusted version before installation; treat the scan result as limited evidence.

Risk: API credentials and any supplied session cookies are sent to the external MaxHub service; cookies can provide account access.

Mitigation: Use the service only if trusted, keep API keys and cookies out of prompts and logs, and use a separate test account for cookie-based endpoints.

## Reference(s):

- [MaxHub Douyin source repository](https://github.com/XieWxx/maxhub-douyin)
- [Server-resolved source commit](https://github.com/XieWxx/maxhub-douyin/commit/78d23799879934caf492b8f859248cc9f3155d48)
- [ClawHub release](https://clawhub.ai/xiewxx/skills/maxhub-douyin-2)
- [MaxHub API service](https://www.aconfig.cn)
- [Video API reference](references/api-video.md)
- [User API reference](references/api-user.md)
- [Search API reference](references/api-search.md)
- [Trending API reference](references/api-trending.md)
- [Creator API reference](references/api-creator.md)
- [Xingtu API reference](references/api-xingtu.md)
- [Index and analytics API reference](references/api-index.md)
- [Parameter mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown summaries and tables based on API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses follow the user's language and use human-readable number formats.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
