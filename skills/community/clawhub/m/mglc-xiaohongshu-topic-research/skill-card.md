## Description:

围绕小红书内容赛道或关键词，结合搜索结果、笔记正文和按需评论形成选题建议、标题方向、内容提纲与参考案例。适合为账号制定有真实样本依据的内容计划。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

面向运营小红书账号的内容创作者与营销人员，按关键词或指定笔记研究公开样本，并据此整理选题、标题方向、内容提纲和参考案例。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 安全扫描报告了权限范围问题，且部分引用路径无法分析，因此安全证据不完整。

Mitigation: 运行前审阅技能所需的网络与 API 访问范围；将 API 密钥保存在本机，不发送到聊天或报告中。

Risk: 查询会按客户价格产生 API 费用。

Mitigation: 执行前查看本次费用估算，并使用用户已授权的预算上限。

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dunkong/skills/mglc-xiaohongshu-topic-research)
- [参数与分页](references/usage.md)
- [分析与证据格式](references/analysis.md)
- [示例计划](references/example-plan.json)
- [曼格云 API Key 服务](https://api.we-media.cn?source=clawhub&skill=mglc-xiaohongshu-topic-research)

## Skill Output:

**Output Type(s):** [Analysis, Markdown reports, JSON, CSV, HTML reports, Excel spreadsheets]

**Output Format:** [基于检索样本的中文选题建议与报告文件；支持 Markdown、HTML、JSON、CSV 和可选 Excel]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [选题理由引用实际样本；未取得的数值与范围缺口保持明确，不推断趋势或爆款保证。]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
