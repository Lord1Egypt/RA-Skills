## Description:

亚马逊广告体检与开投：用搜索词报告算出零单花费占比、验证通行否词常识在本账户成不成立，再按意图结构决定预算怎么分。接领霄官网 MCP，扔一张搜索词报告就出结果。当用户要开亚马逊广告、做广告优化、否词、判断广告钱花在哪、问"网上说的那套对不对"、分析搜索词报告时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeli20221102-ux](https://clawhub.ai/user/mikeli20221102-ux)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and advertising operators use this skill to analyze uploaded Amazon search term reports, identify zero-order spend, and test account-specific keyword optimization assumptions. It also guides budget structure across harvesting, defensive, and exploration advertising intent layers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amazon advertising reports may contain confidential spend, sales, campaign, keyword, or product data.

Mitigation: Inspect CSV contents before upload, remove unnecessary columns, and submit reports only after accepting processing by the third-party Lingxiao service.

Risk: The skill connects users to a mutable third-party MCP server for report analysis.

Mitigation: Use a project-scoped MCP configuration where possible and allow only the named tools if the client supports tool allowlisting.

Risk: Search term report interpretation can lead to harmful keyword or budget changes if conclusions are overgeneralized.

Mitigation: Keep the skill's stated boundaries with results: do not bulk-negative keywords across groups, do not infer profitability without cost data, and compare only within the user's account.

## Reference(s):

- [Lingxiao MCP endpoint](https://www.lingxiaochuhai.com/mcp)
- [Ads waste check tool](https://www.lingxiaochuhai.com/tools/ads-waste-check)
- [Ads myth check tool](https://www.lingxiaochuhai.com/tools/ads-myth-check)
- [ClawHub skill page](https://clawhub.ai/mikeli20221102-ux/skills/lingxiao-amazon-ads-check)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON MCP configuration and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on user-provided Amazon advertising reports and the connected third-party Lingxiao MCP service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
