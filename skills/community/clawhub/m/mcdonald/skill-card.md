## Description:

Mcdonald helps agents query and claim McDonald's coupons, check activity calendars, and review nutrition information through the McDonald's MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hi-yu](https://clawhub.ai/user/hi-yu)

### License/Terms of Use:


## Use Case:

External users can ask an agent to find available McDonald's coupons, claim coupons, check current promotions, and present menu nutrition information. The skill is also useful for agents that need to format coupon and nutrition results for quick comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens can be exposed or sent to an untrusted endpoint if MCD_TOKEN or MCD_MCP_URL is mishandled.

Mitigation: Use only a trusted McDonald's MCP token, avoid displaying the token, and keep MCD_MCP_URL unset unless the alternate endpoint is fully trusted.

Risk: One-click coupon claiming can modify the user's McDonald's account state.

Mitigation: Require user confirmation before calling auto-bind-coupons or any action that claims coupons.

Risk: Coupon and campaign data can change quickly and may be rate limited by the service.

Mitigation: Query the service at the time of use and avoid repeated high-frequency requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hi-yu/skills/mcdonald)
- [McDonald's MCP service](https://mcp.mcd.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted MCD_TOKEN and may use MCD_MCP_URL only when the alternate endpoint is trusted.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
