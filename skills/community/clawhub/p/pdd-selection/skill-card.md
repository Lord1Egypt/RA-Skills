## Description: <br>
零配置即装即用，提供拼多多商品搜索、商品详情和频道好货浏览3项工具，支持百亿补贴、秒杀、销量榜等频道，返回优惠价格、优惠券和购买链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping assistants use this skill to search Pinduoduo products, inspect item details, and browse deal channels such as 百亿补贴, 秒杀, and 销量榜. It supports product discovery and comparison within Pinduoduo, but it does not place orders or access account, order, or logistics data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping queries are forwarded through a disclosed cloud proxy to retrieve Pinduoduo product data. <br>
Mitigation: Avoid private or sensitive search terms and review the proxy data flow before use. <br>
Risk: Product prices, coupons, availability, and item details can change in real time. <br>
Mitigation: Confirm specifications, seller details, coupon terms, and final checkout price on Pinduoduo before acting on results. <br>
Risk: The skill returns product information and purchase links, but does not complete purchases or access orders. <br>
Mitigation: Use it for discovery only; complete any purchase review and checkout outside the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-shopping/pdd-selection) <br>
- [Publisher profile](https://clawhub.ai/user/cn-shopping) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON object containing a human-readable Chinese text response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product names, prices, coupons, sales labels, image URLs, goods_sign identifiers, and purchase links when returned by the upstream product data service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
