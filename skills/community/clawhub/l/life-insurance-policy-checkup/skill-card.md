## Description:

帮助寿险保险代理人整理家庭保单、核对保障责任与待补资料，并生成客户摘要和顾问跟进建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dm-kevin](https://clawhub.ai/user/dm-kevin)

### License/Terms of Use:

MIT-0

## Use Case:

寿险保险代理人依据客户提供的保单材料整理家庭现有保障、识别待核对事项，并准备客户可读的体检摘要和顾问后续沟通建议。

### Deployment Geography for Use:

China (mainland)

## Known Risks and Mitigations:

Risk: 保单、健康和身份资料可能含敏感个人信息。

Mitigation: 上传前遮盖身份标识、完整保单号与联系方式；只提供检视所需资料，不向服务商自动分享。

Risk: 材料不完整或条款理解有误可能导致错误的保障或退休资金结论。

Mitigation: 标明材料范围和待核对事项，以正式合同、批单和保险公司确认结果复核；缺少现金流资料时不量化养老缺口。

Risk: 微信服务咨询入口属于商业联系渠道，可能被误认为独立推荐。

Mitigation: 仅经用户同意后展示，并明确其商业联系性质；核实服务提供方、适用条件和价格。

## Reference(s):

- [ClawHub 技能页面](https://clawhub.ai/dm-kevin/skills/life-insurance-policy-checkup)
- [保单检视规则](references/checkup-rules.md)
- [输出参考](references/report-template.md)
- [保险销售行为管理办法](https://www.nfra.gov.cn/cn/view/pages/ItemDetail.html?docId=1129945&itemId=928)
- [关于规范短期健康保险业务有关问题的通知](https://www.nfra.gov.cn/cn/view/pages/ItemDetail.html?docId=958198)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [中文 Markdown，含保单汇总表、客户摘要及按需提供的顾问建议]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [资料不全时标注待核对项；只要求客户版时省略内部建议。]

## Skill Version(s):

1.1.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
