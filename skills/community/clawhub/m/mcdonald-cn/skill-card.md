## Description: <br>
麦当劳助手 - 查询/领取优惠券、活动日历、餐品营养信息、门店查询 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hi-yu](https://clawhub.ai/user/hi-yu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to query McDonald's China coupons, promotions, nutrition information, store information, and meal options through the configured MCP service. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses MCD_TOKEN to authenticate against the MCP service. <br>
Mitigation: Keep MCD_TOKEN private, avoid logging or pasting it into public chats, and install only when the configured MCP endpoint is trusted. <br>
Risk: The skill can claim coupons through the one-click coupon workflow. <br>
Mitigation: Ask the agent to list available coupons and get clear confirmation before invoking coupon claiming. <br>
Risk: Coupon, promotion, and campaign data can change quickly. <br>
Mitigation: Query the live service close to the time of use and present validity dates or conditions when available. <br>


## Reference(s): <br>
- [McDonald's China MCP service](https://mcp.mcd.cn) <br>
- [ClawHub release page](https://clawhub.ai/hi-yu/mcdonald-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and optional tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MCD_TOKEN; may use MCD_MCP_URL; coupon, promotion, and nutrition responses depend on the live MCP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
