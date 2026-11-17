## Description:

麦当劳助手 - 查询/领取优惠券、活动日历、餐品营养信息、门店查询

This skill is ready for commercial/non-commercial use.

## Publisher:

[hi-yu](https://clawhub.ai/user/hi-yu)

### License/Terms of Use:


## Use Case:

Consumers and food-service assistants use this skill to query McDonald's coupons, activity calendars, nutrition information, and related time-sensitive offers through the configured MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an account token for remote MCP requests.

Mitigation: Install only if the MCP service and token issuer are trusted, keep MCD_TOKEN private, and avoid exposing it in logs or shared terminals.

Risk: Coupon-claiming actions can modify account state.

Mitigation: Ask for explicit user confirmation before running auto-bind-coupons or other account-changing calls.

Risk: The configurable MCD_MCP_URL can redirect requests to another service.

Mitigation: Use the default HTTPS endpoint or set MCD_MCP_URL only to an explicitly trusted HTTPS URL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hi-yu/skills/mcd)
- [Publisher profile](https://clawhub.ai/user/hi-yu)
- [McDonald's MCP service](https://mcp.mcd.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with JSON-RPC curl command examples and tabular summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided MCD_TOKEN for authenticated MCP requests.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
