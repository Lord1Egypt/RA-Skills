## Description:

用既有 ASIN 的商品详情与评论证据，检查 Amazon 商品改版或重新上线的准备度与风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

面向管理 Amazon 既有 ASIN 的卖家和运营人员，依据商品详情与评论评估改版或重新上线前的风险。适用于已有 ASIN 和评论证据，不用于全新品预测、广告预算或供应链执行。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 此重新上线检查技能同时暴露自动积点消费和周期采集，但审批控制不一致。

Mitigation: 优先使用落实专用重新上线工作流的修正版；若继续使用，将账户扣费设为每次确认，明确要求免费报价，单次任务选择手动采集，并检查现有采集计划及竞品订阅。

## Reference(s):

- [操作工作流](references/operation-workflow.md)
- [ARI CLI 与 API 参考](references/reference.md)
- [ARI 操作工作台](https://ari.funewa.com/zh/operations)
- [ARI 监控中心](https://ari.funewa.com/zh/monitor)
- [ClawHub 发布页](https://clawhub.ai/funewa/skills/launch-readiness)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [结构化 Markdown 上线准备度评估（ops_audit）]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [基于已有商品详情和评论证据；评论不足时说明数据缺口，不隐式采集。]

## Skill Version(s):

1.5.3 (source: release evidence, CHANGELOG.md, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
