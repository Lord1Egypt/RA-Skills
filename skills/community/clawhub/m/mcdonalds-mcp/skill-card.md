## Description:

麦当劳MCP服务集成，支持点餐、优惠券、麦麦商城、积分兑换等功能。需要用户先在 https://open.mcd.cn 申请MCP Token。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessiondai](https://clawhub.ai/user/jessiondai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent or CLI workflow to McDonald's MCP services for menu lookup, coupon operations, points exchange, delivery address management, and order creation after supplying their own MCP token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A McDonald's MCP token may be exposed when passed directly as a command-line argument.

Mitigation: Avoid pasting real tokens into shell history or shared terminals; rotate any token that may have been exposed.

Risk: The create_order and create_exchange_order methods can initiate real account actions or transactions.

Mitigation: Require explicit user confirmation before invoking order or points-exchange methods.

## Reference(s):

- [McDonald's MCP Open Platform](https://open.mcd.cn)
- [McDonald's MCP Endpoint](https://mcp.mcd.cn)
- [ClawHub Skill Page](https://clawhub.ai/jessiondai/skills/mcdonalds-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with JavaScript CLI commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided MCP token; create_order and create_exchange_order can initiate real transactions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
