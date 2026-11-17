## Description:

麦当劳中国 MCP 服务集成，支持优惠券、点餐、外卖、积分商城等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongdeyu](https://clawhub.ai/user/kongdeyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill with a McDonald's China account token to query coupons, menus, account points, delivery addresses, create delivery orders, and redeem points.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can use an account token to place orders, redeem points, claim coupons, and manage delivery addresses.

Mitigation: Review before installing and require explicit confirmation before placing orders, redeeming points, creating addresses, or bulk claiming coupons.

Risk: Delivery addresses and phone numbers may be exposed through tool calls and responses.

Mitigation: Treat delivery addresses and phone numbers as sensitive personal data and avoid sharing outputs beyond the account holder's intended workflow.

## Reference(s):

- [McDonald's China MCP portal](https://open.mcd.cn/mcp)
- [McDonald's China MCP endpoint](https://mcp.mcd.cn)
- [McDonald's MCP tools reference](references/tools.md)
- [ClawHub skill page](https://clawhub.ai/kongdeyu/skills/mcdonalds)
- [Publisher profile](https://clawhub.ai/user/kongdeyu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON arguments or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MCD_MCP_TOKEN for authenticated McDonald's China MCP requests.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
