## Description:

帮助用户检索和分析全国招标采购公告、企业信息、供应商及市场数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

面向采购、商务和市场研究人员，按需查询招标、中标、采购意向、企业及市场数据，并整理成分析结果。

### Deployment Geography for Use:

中国

## Known Risks and Mitigations:

Risk: 搜索词和企业标识会发送给知了标讯；外部服务的隐私实践和运行时行为未经验证。

Mitigation: 查询前告知用户数据会发送至该服务，只提交完成所需查询的关键词和标识；涉及敏感数据时先核实服务方隐私条款。

Risk: 部分成功查询会消耗账户积分。

Mitigation: 按用户所需范围调用，避免不必要的关联查询或翻页，并在需要时先查看账户余额。

Risk: API Key 和临时登录链接可能允许访问账户。

Mitigation: 妥善保管密钥和临时链接，不在回复或共享文件中暴露。

Risk: 未配置 API Key 时的可选自动注册会收集设备特征。

Mitigation: 开始收集前先取得用户同意；用户不同意时停止该流程并提供手动申请入口。

## Reference(s):

- [标讯搜索 API 参考](artifact/references/api-search.md)
- [企业分析 API 参考](artifact/references/api-company.md)
- [市场分析 API 参考](artifact/references/api-market.md)
- [工商数据 API 参考](artifact/references/api-registry.md)
- [账户查询 API 参考](artifact/references/api-account.md)
- [注册与隐私流程参考](artifact/references/auto-register.md)
- [ClawHub 技能页面](https://clawhub.ai/zhiliaobiaoxun/skills/national-procurement-bidding-net-chinabidding)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [中文 Markdown 摘要、列表和表格]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [按用户指定范围查询；部分查询可能消耗积分。]

## Skill Version(s):

1.0.10 (source: frontmatter; server release 1.0.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
