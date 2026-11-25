## Description:

快手达人筛选提供快手公开视频搜索、博主作品与粉丝数据及视频评论，并以结构化 JSON 返回结果；无需登录或发布内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

外部营销人员、内容创作者和数据分析人员可用此技能查找快手创作者、查看公开作品与粉丝数据、评估互动表现，并探索内容选题或评论舆情。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and links are sent to the third-party guaikei.com service.

Mitigation: Send only intended public Kuaishou keywords and links; avoid including sensitive information.

Risk: The security scan reports that 12 of 34 components were only partially inspected and that tool scope and installation fit need attention.

Mitigation: Review the skill and its requested environment requirements before installation, and limit use to the intended read-only Kuaishou queries.

## Reference(s):

- [参数选项](artifact/references/options.md)
- [常见问题](artifact/references/faq.md)
- [快手数据 API 与令牌信息](https://www.guaikei.com)
- [ClawHub 技能发布页](https://clawhub.ai/guaikei/skills/ks-koc)
- [发布者资料](https://clawhub.ai/user/guaikei)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON result envelope containing search results, creator data, or comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; available result counts depend on the token plan.]

## Skill Version(s):

1.1.3 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
