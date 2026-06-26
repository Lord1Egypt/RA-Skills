## Description: <br>
McDonald's China coupon redemption, query, and points checking for coupon management, points mall actions, campaign calendar lookup, delivery ordering, and nutrition information through McDonald's China MCP services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chandler0714](https://clawhub.ai/user/chandler0714) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage McDonald's China coupons and points, inspect campaign, menu, nutrition, and account information, and prepare or create delivery orders tied to a configured McDonald's China account token. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a McDonald's China account token to read account, coupon, points, address, and delivery-order information. <br>
Mitigation: Use a temporary environment variable or secure credential manager, and avoid entering the token on shared, logged, synced, or screen-shared machines. <br>
Risk: The skill can perform account-changing actions such as claiming coupons, spending points, changing delivery addresses, and creating orders. <br>
Mitigation: Require explicit user confirmation before any coupon claim, points redemption, address change, price calculation that leads to checkout, or order creation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chandler0714/mstore) <br>
- [McDonald's China MCP token portal](https://open.mcd.cn/mcp) <br>
- [McDonald's China MCP server](https://mcp.mcd.cn) <br>
- [McDonald's China MCP API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided MCDCN_MCP_TOKEN for account-specific actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
