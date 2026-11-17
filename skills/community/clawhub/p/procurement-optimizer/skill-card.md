## Description:

根据采购需求与供应商报价，按包装、交期、容量和运费整理整数拆单方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

面向采购人员，帮助整理需求与报价，计算并核对整数拆单及商品金额、运费和总额；求解前由用户确认数据和费用，结果仅供采购决策参考。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplier quotes and procurement details are sent to an external service, and private projects are retained for 30 days.

Mitigation: Use only user-authorized data, minimize uploads, and confirm the provider's privacy and retention terms.

Risk: Paid solving incurs service charges that may change.

Mitigation: Verify the current price and expected total, then obtain user approval before solving.

## Reference(s):

- [平台首页](https://ai-skills.open-idea.net)
- [采购工作台](https://ai-skills.open-idea.net/dashboard/products/procurement-optimizer)
- [平台密钥与费用](https://ai-skills.open-idea.net/skill-docs/procurement-optimizer/API-KEY.md)
- [请求、上传和续查](https://ai-skills.open-idea.net/skill-docs/procurement-optimizer/HTTP-REQUESTS.md)
- [操作字段与规则](https://ai-skills.open-idea.net/skill-docs/procurement-optimizer/OPERATIONS.md)
- [授权、隐私与人工确认](https://ai-skills.open-idea.net/skill-docs/procurement-optimizer/BEHAVIOR-RULES.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, JSON, Markdown, Shell commands]

**Output Format:** [Markdown summaries, JSON request data, and service export files (XLSX, JSON, Markdown)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CNY, tax-inclusive, single delivery address, integer quantities; export requires a verified OPTIMAL or FEASIBLE result. FEASIBLE is not proven optimal.]

## Skill Version(s):

1.1.0 (source: SKILL.md packageVersion, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
