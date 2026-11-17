## Description:

Helps agents search Luogang products, retrieve product details, and return purchase links when users show shopping intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fireium](https://clawhub.ai/user/fireium)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to search Luogang ecommerce listings, review product details such as price and availability, and provide links for purchase handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping searches and product-detail requests are sent to the external Luogang MCP service.

Mitigation: Install only when that external service use is acceptable, and confirm the user wants Luogang results before using the skill for generic shopping requests.

Risk: Product availability, prices, and links may depend on live service responses.

Mitigation: Present returned product information as current service output and guide users to verify final purchase details at the linked checkout or product page.

## Reference(s):

- [Luogang MCP service endpoint](https://yuju-mcp.wxhoutai.com/mcp)
- [Luogang H5 product detail example](https://eshop.wxhoutai.com/h5/pages/goods/detail?goods_id=xxx)
- [ClawHub skill page](https://clawhub.ai/fireium/skills/luogang-shopping-assistant)
- [ClawHub publisher profile](https://clawhub.ai/user/fireium)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples and product-result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product search output is intended to summarize up to 10 candidates and include purchase or detail links when available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
