## Description:

TikTok 数据查询与创作者分析 skill，通过 MaxHub API 查询视频详情、评论、用户资料、搜索、趋势、广告/商店/创作者数据端点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

TikTok 内容创作者、营销人员和数据分析人员可用它查询公开视频、用户、评论、搜索趋势、广告及 TikTok Shop 数据，并整理成选题、竞品和创作者分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags upgrade guidance that may prompt updates and requests beyond the documented API boundary.

Mitigation: Pin reviewed skill and package versions, require explicit approval before upgrades, restrict outbound access to the verified API host, and do not send credentials to upgrade or CDN destinations.

Risk: The security review reports local legal-confirmation records that can assert consent or review without verified confirmation.

Mitigation: Verify consent directly with the user and remove or correct any unverified confirmation records before relying on them.

Risk: Requests send an API key and user-supplied identifiers, keywords, or URLs to the third-party MaxHub service; optional cookies or tokens are also listed as transmissible inputs.

Mitigation: Use only authorized, minimal inputs, avoid supplying cookies or tokens, and keep API credentials scoped to the trusted API host.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-tiktok)
- [MaxHub API service](https://www.aconfig.cn)
- [SkillHub listing](https://skillhub.cn/skills/tiktok-pro)
- [TikTok developer documentation](https://developers.tiktok.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Analysis, Guidance]

**Output Format:** [Text or Markdown summaries with structured JSON data and analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected API endpoint and supplied query parameters.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
