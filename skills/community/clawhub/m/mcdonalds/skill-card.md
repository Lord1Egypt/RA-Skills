## Description: <br>
麦当劳中国 MCP 服务集成，支持优惠券、点餐、外卖、积分商城等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongdeyu](https://clawhub.ai/user/kongdeyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
麦当劳中国用户可以让代理查询优惠券、菜单、配送地址、订单、积分账户和积分商城商品，并通过 MCP 工具辅助外卖下单或积分兑换。 <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to a live McDonald's China account token. <br>
Mitigation: Install only if this account access is acceptable, keep MCD_MCP_TOKEN private, and avoid exposing token values in prompts, logs, or shared output. <br>
Risk: Order creation, point redemption, address changes, and bulk coupon claims can affect the user's account, money, delivery details, or points balance. <br>
Mitigation: Require the assistant to show the exact items, address, store, price, fees, coupons, and points impact, then approve each sensitive action explicitly before it is executed. <br>


## Reference(s): <br>
- [麦当劳 MCP 工具参考](artifact/references/tools.md) <br>
- [麦当劳中国 MCP](https://open.mcd.cn/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/kongdeyu/mcdonalds) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with bash examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MCD_MCP_TOKEN for live McDonald's China account access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
