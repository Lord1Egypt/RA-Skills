## Description:

查询快手公开视频、账号作品和评论数据，并据此为账号诊断与竞品分析提供结构化依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

面向快手内容运营人员、创作者和营销团队，用于发现关键词热点、查看公开账号作品与互动数据、分析视频评论，并整理账号诊断和内容运营建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 查询关键词或快手视频、主页链接会发送至瓜客网服务处理。

Mitigation: 仅提交可公开查询且不含敏感信息的关键词与链接；运行前确认接受该第三方处理方式。

Risk: 运行需要 GUAIKEI_API_TOKEN，且安全审查对部分组件的分析不完整。

Mitigation: 只在受信任的本地环境配置令牌，并在使用前核对命令及其外部调用范围。

## Reference(s):

- [命令参数说明](references/options.md)
- [更新日志](references/changelog.md)
- [瓜客网服务与令牌开通](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [结构化 JSON 数据及简洁的 Markdown 账号分析与运营建议]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [仅包含快手公开数据；返回条数受 API 套餐和命令上限约束。]

## Skill Version(s):

1.1.2 (source: release metadata, SKILL.md, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
