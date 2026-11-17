## Description:

查询 B 站视频、用户、评论、弹幕和直播数据，并支持 App 与 Web 双端 API。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to query and analyze Bilibili videos, creator profiles, comments, danmaku, search results, and live data through MaxHub APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bilibili workflow includes fallback paths for Douyin endpoints, which may not fit the requested platform scope.

Mitigation: Use documented Bilibili endpoints and verify that an alternate-platform fallback is needed before using it.

Risk: The documented installer command does not pin a release, so the installed contents may change.

Mitigation: Review the package source and version before installation.

Risk: API requests send credentials to MaxHub, and some endpoints require platform session cookies.

Mitigation: Provide cookies only when the service is trusted; prefer scoped credentials, use a separate test account when possible, and rotate or revoke cookies after use.

## Reference(s):

- [Video Data API](references/api-video.md)
- [User Data API](references/api-user.md)
- [Search and Feed API](references/api-search.md)
- [Live and Comment API](references/api-live.md)
- [Parameter Mappings](references/param-mappings.md)
- [Source repository](https://github.com/XieWxx/maxhub-bilibili)
- [MaxHub API service](https://www.aconfig.cn)
- [ClawHub release](https://clawhub.ai/xiewxx/skills/maxhub-bilibili-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Concise summaries and Markdown tables, in Chinese or English]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect data returned by the API.]

## Skill Version(s):

0.1.0 (server-resolved release; artifact metadata also lists 3.6.1 and 3.6.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
