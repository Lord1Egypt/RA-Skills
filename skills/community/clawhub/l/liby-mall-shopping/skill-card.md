## Description: <br>
立白龙虾购是立白官方商城服务，支持获得立乐家积分、商品搜索、下单、订单管理、物流查询等操作，还能解答洗衣清洁问题（如咖啡渍、油渍、梅雨天衣物护理等），提供立白产品购买渠道和优惠信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[softgoto](https://clawhub.ai/user/softgoto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to browse Liby mall products, manage points, place confirmed orders, check orders and logistics, contact customer service, and receive laundry-care guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive login, address, order, and payment-related actions are routed through an unpinned external npm command with unclear provenance. <br>
Mitigation: Install only after trusting the publisher and verifying `@libydic/mall` is the legitimate Liby mall tool. <br>
Risk: Mall actions may involve personal details, phone codes, address information, points, cash payments, and order creation. <br>
Mitigation: Confirm products, prices, points and cash requirements, addresses, and orders before payment; avoid sharing phone codes or address details unless the login flow and package provenance are clear. <br>
Risk: Broad activation triggers can start shopping or account workflows in ordinary conversations. <br>
Mitigation: Use the skill intentionally for mall tasks and keep the user involved before login, address changes, order creation, or payment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/softgoto/liby-mall-shopping) <br>
- [Publisher profile](https://clawhub.ai/user/softgoto) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or short text responses with shell command invocations and media-send guidance when images are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce login, order, address, points, logistics, payment, and customer-service guidance based on tool results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
