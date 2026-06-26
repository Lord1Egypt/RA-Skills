## Description: <br>
麦当劳 MCP 点餐技能。通过麦当劳官方 MCP 服务查询门店、餐品、优惠券，完成外送/到店/团餐点餐与积分兑换。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meteorsliu](https://clawhub.ai/user/meteorsliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Consumers in mainland China use this skill with OpenClaw and a McDonald's China MCP token to query stores, menus, coupons, orders, nutrition, and loyalty-point redemption options. It guides delivery, pickup, group meal, coupon, and points-redemption workflows while asking for user confirmation before order or redemption actions. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided McDonald's China MCP token that represents the user's account identity. <br>
Mitigation: Treat the token as an account credential, do not share it, and install the skill only when OpenClaw should use that token for McDonald's China actions. <br>
Risk: Address creation, coupon claiming, order creation, and points redemption can change account state or start a purchase flow. <br>
Mitigation: Review the address, store, items, price, coupons, order details, and points impact before approving those actions. <br>


## Reference(s): <br>
- [McDonald's China MCP Portal](https://open.mcd.cn/mcp) <br>
- [McDonald's China MCP Documentation](https://open.mcd.cn/mcp/doc) <br>
- [McDonald's China MCP Server](https://mcp.mcd.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/meteorsliu/mcdonalds-mcp-china) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with command examples, JSON configuration snippets, and MCP tool call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided McDonald's China MCP token and explicit user review of account, address, coupon, price, order, and points-redemption effects.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
