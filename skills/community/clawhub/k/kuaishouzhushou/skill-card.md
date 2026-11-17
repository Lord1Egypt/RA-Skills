## Description:

搜索快手公开视频、获取博主公开作品与视频评论，并返回结构化数据供内容调研与分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

快手内容创作者、运营人员和品牌营销者可用它搜索公开视频、查看博主公开作品与评论，并将结构化结果用于选题、竞品和舆情分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keywords and links are sent to www.guaikei.com to retrieve public Kuaishou data.

Mitigation: Avoid confidential query terms or links, and use only inputs you are authorized to share.

Risk: The security review was partial: 20 of 32 components were fully scanned, with 12 only partially inspected.

Mitigation: Review the partially inspected scripts before installation if their behavior is material to your use.

## Reference(s):

- [参数选项说明](references/options.md)
- [更新日志](references/changelog.md)
- [快手运营助手官网](https://www.guaikei.com)
- [ClawHub 技能页面](https://clawhub.ai/why20261/skills/kuaishouzhushou)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON records for video search results, creator posts, or video comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fields and interaction metrics vary by command; results are limited to public Kuaishou data.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter, package.json, changelog, released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
