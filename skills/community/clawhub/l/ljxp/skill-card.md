## Description:

蓝鲸选品助手-text supports Mercado Libre product-selection and operations analysis across Mexico, Brazil, Argentina, Chile, and Colombia by calling the LJXP API through local scripts for product, category, keyword, pricing, competitor, seller, brand, catalog, shipping, and exchange-rate data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nlikeso](https://clawhub.ai/user/nlikeso)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators, sellers, and analysts use this skill to research Mercado Libre categories, products, keywords, competitors, sellers, catalog links, shipping costs, and margins. It helps agents turn LJXP API results into concise market analysis, business conclusions, and next-step recommendations.

### Deployment Geography for Use:

Mexico, Brazil, Argentina, Chile, and Colombia marketplace sites

## Known Risks and Mitigations:

Risk: The skill can use an LJXP API token to query commercial marketplace data.

Mitigation: Use LJXP_TOKEN instead of passing tokens on the command line, and avoid exposing tokens in prompts, shell history, logs, or shared terminals.

Risk: Optional HTML output can save full marketplace research locally and may open browser rendering.

Mitigation: Use HTML output only when browser rendering is intended, and delete generated ljxp_search HTML files if they contain sensitive business research.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nlikeso/skills/ljxp)
- [Publisher profile](https://clawhub.ai/user/nlikeso)
- [深圳领东时代科技有限公司](https://www.lingdongsz.com/)
- [蓝鲸选品 Skill 服务页](https://xp.lingdongsz.com/#/skillServer)
- [蓝鲸选品 API 参考索引](references/api_reference.md)
- [商品接口参考](references/api/items.md)
- [行业趋势接口参考](references/api/trends.md)
- [用户套餐与积分参考](references/api/users.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Files, Guidance]

**Output Format:** [Markdown analysis with tables, command snippets, and optional generated HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an LJXP API token for data queries; HTML output may create local ljxp_search files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
