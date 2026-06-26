## Description: <br>
麦当劳助手可帮助用户查询和领取优惠券、查看活动日历、查询餐品营养信息和门店信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hi-yu](https://clawhub.ai/user/hi-yu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can ask an agent for current McDonald's coupons, promotions, nutrition details, and related account coupon information through the disclosed MCP service. The skill can also guide coupon claiming when the user provides a valid token and wants the agent to modify account coupons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided MCD_TOKEN for account-specific coupon queries and coupon claiming. <br>
Mitigation: Keep MCD_TOKEN private and install only if you trust the disclosed McDonald's MCP service. <br>
Risk: Changing MCD_MCP_URL or enabling one-click coupon claiming can send requests to an unintended endpoint or modify account coupons. <br>
Mitigation: Leave MCD_MCP_URL at the default unless another HTTPS endpoint is intentionally verified, and allow one-click claiming only when the user wants coupons added to the account. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hi-yu/mcd) <br>
- [McDonald's MCP Service](https://mcp.mcd.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown responses with optional tables and JSON-RPC curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided MCD_TOKEN for account-specific coupon queries or claiming.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter remains 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
