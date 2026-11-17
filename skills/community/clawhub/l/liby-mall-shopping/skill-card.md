## Description:

立白龙虾购是立白官方商城服务，支持获得立乐家积分、商品搜索、下单、订单管理、物流查询等操作，还能解答洗衣清洁问题（如咖啡渍、油渍、梅雨天衣物护理等），提供立白产品购买渠道和优惠信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[softgoto](https://clawhub.ai/user/softgoto)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to browse Liby mall products, check points, manage delivery addresses, place confirmed orders, and query orders or logistics. It also helps users with laundry and cleaning questions tied to Liby products, purchasing channels, and promotions.

### Deployment Geography for Use:

Mainland China for shopping and fulfillment; general product and laundry guidance may be used more broadly.

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm package for login, address, order, and points operations, so runtime behavior may change after review.

Mitigation: Pin or otherwise govern the package version, review the package before installation, and run it in a sandboxed runtime.

Risk: The skill handles sensitive account, phone, address, order, payment, and points data.

Mitigation: Require explicit user confirmation before login, address access, address creation, and order creation; clear session-related data when users switch or exit accounts.

Risk: Shopping actions can create orders or payment flows if the agent proceeds without enough user confirmation.

Mitigation: Confirm the selected product, address, delivery rules, and combined points-plus-cash price before creating an order.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/softgoto/skills/liby-mall-shopping)
- [Publisher profile](https://clawhub.ai/user/softgoto)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with inline shell command examples and JSON media payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return user-facing shopping, points, order, logistics, customer-service, payment, and image-response guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
