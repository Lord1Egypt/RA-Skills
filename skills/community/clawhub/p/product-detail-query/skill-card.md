## Description:

根据保险产品名称自动匹配版本，查询并返回对应的详细产品参数和配置说明。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangbaiqi521](https://clawhub.ai/user/wangbaiqi521)

### License/Terms of Use:

MIT-0

## Use Case:

外部用户和保险产品支持人员可用此技能按产品名称查询保险产品详情。代理会匹配产品编码和二级分类 ID，调用公开的产品详情 API，并返回对应版本的信息。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product identifiers are sent to the disclosed hongdibaobei.com product-detail API.

Mitigation: Confirm that the user is comfortable sending product identifiers to that API before installation or use.

Risk: When a product name has multiple versions, automatically choosing the first match may return details for the wrong insurance plan.

Mitigation: Ask the agent to list or confirm matching versions before relying on results for insurance decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangbaiqi521/skills/product-detail-query)
- [Product detail API endpoint](https://openapi-test.hongdibaobei.com/v1/chat/robot/product/detail)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown summary with JSON API output when the script is invoked]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May identify the selected product version when multiple matches are found.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
