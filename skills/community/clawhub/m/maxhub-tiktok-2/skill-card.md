## Description:

TikTok 数据查询与工具助手，覆盖视频详情、用户数据、搜索、广告、创作者工具和电商数据，并包含已标注的部分交互触发与协议工具接口。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

跨境营销团队、品牌运营人员和创作者研究人员可用它通过 MaxHub API 查询 TikTok 视频、用户、搜索、广告、创作者及电商数据，并整理结果用于趋势比较和分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial ClawScan review flags platform-scope mismatches and an unlabeled view-count operation.

Mitigation: Clarify the platform fallbacks and view-count operation, pin the installer version, and verify the API destination before installation, as the security guidance recommends.

Risk: The skill requires an API key and documents optional session-cookie use with the third-party API service.

Mitigation: Verify the service before sending credentials. Keep the API key private; provide a session cookie only when necessary, use a separate test account, and revoke the session after use.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-tiktok)
- [MaxHub API service](https://www.aconfig.cn)
- [Video API reference](artifact/references/api-video.md)
- [User API reference](artifact/references/api-user.md)
- [Search API reference](artifact/references/api-search.md)
- [Ads and analytics API reference](artifact/references/api-ads-analytics.md)
- [Parameter mappings](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Chinese or English text, with Markdown tables and concise summaries when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language and formats large numbers accordingly; may include API setup and error guidance.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
