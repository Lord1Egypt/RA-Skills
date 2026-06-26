## Description: <br>
麦当劳MCP服务集成，支持点餐、优惠券、麦麦商城、积分兑换等功能。需要用户先在 https://open.mcd.cn 申请MCP Token。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessiondai](https://clawhub.ai/user/jessiondai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to McDonald’s MCP services for menu lookup, coupon actions, delivery ordering, account address management, points lookup, and points redemption after providing their own MCP token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a McDonald’s MCP token for actions that spend money, redeem points, claim coupons, or change account data. <br>
Mitigation: Require explicit user approval after showing exact order contents, delivery address, coupon action, points cost, and total price before any state-changing call. <br>
Risk: The MCP token grants account access and could be exposed through prompts, logs, command history, or shared agent context. <br>
Mitigation: Keep the token private and revocable, avoid storing it in shared files or transcripts, and rotate it if exposure is suspected. <br>
Risk: Unverified parameters may create incorrect orders, addresses, coupon claims, or redemptions. <br>
Mitigation: Start with read-only queries, validate returned item identifiers and account details, and require confirmation before create, add, receive, or redeem operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jessiondai/mcdonalds-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/jessiondai) <br>
- [McDonald’s MCP token portal](https://open.mcd.cn) <br>
- [McDonald’s MCP endpoint](https://mcp.mcd.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript helper code, shell command examples, and JSON API responses from MCP calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided McDonald’s MCP token; API requests are sent to https://mcp.mcd.cn and may read or modify account state depending on the selected method.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
