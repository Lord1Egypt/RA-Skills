## Description: <br>
麦当劳助手 - 查询/领取优惠券、活动日历、餐品营养信息、门店查询 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pmwalkercao](https://clawhub.ai/user/pmwalkercao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to ask an agent for McDonald's coupon, promotion, nutrition, meal-combination, and store-related information through a McDonald's MCP service. The skill can also help claim available coupons when the user has configured a McDonald's MCP token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a McDonald's MCP token to access account-specific coupon data. <br>
Mitigation: Keep MCD_TOKEN private and only configure it in trusted local or secret-managed environments. <br>
Risk: Claiming coupons changes the user's McDonald's account state. <br>
Mitigation: Require clear user confirmation before executing actions that claim all available coupons. <br>
Risk: Changing MCD_MCP_URL can send requests and tokens to an untrusted service. <br>
Mitigation: Leave MCD_MCP_URL pointed at the trusted McDonald's endpoint unless the user intentionally trusts another service. <br>


## Reference(s): <br>
- [My Mcdonald on ClawHub](https://clawhub.ai/pmwalkercao/mymcdonald) <br>
- [McDonald's MCP service](https://mcp.mcd.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tables or lists for coupon and nutrition results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return text or structured JSON-RPC content from the configured McDonald's MCP endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
