## Description:

京东/淘宝/拼多多商品比价、优惠券查询、口令解析与链接转链省钱助手，帮助用户搜索商品、对比价格、解析电商分享内容并生成优惠购买链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangjiun1](https://clawhub.ai/user/zhangjiun1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to search JD, Taobao/Tmall, and Pinduoduo products, compare coupon-adjusted prices, parse shopping share text, and convert supported product links into promotional links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send shopping queries, pasted share text, and product links to the external service op.squirrel2.cn for processing.

Mitigation: Use the skill only for intended shopping queries and links, and avoid sending private details, credentials, account data, or unrelated personal text.

Risk: Ordinary non-URL user text can be sent for share-code parsing before local filtering.

Mitigation: Have the agent confirm ambiguous or sensitive-looking pasted text before invoking share parsing, or narrow inputs to validated shopping share-code formats.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangjiun1/skills/pricecompare)
- [Publisher profile](https://clawhub.ai/user/zhangjiun1)
- [External shopping API service](https://op.squirrel2.cn)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown-formatted text with product details, coupon information, price comparisons, error guidance, and shopping links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external promotional links and platform-specific shopping metadata returned by the API.]

## Skill Version(s):

1.5.6 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
