## Description:

McDonald's helper for checking and claiming coupons, viewing campaign calendars, looking up nutrition information, and finding stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmwalkercao](https://clawhub.ai/user/pmwalkercao)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve current McDonald's coupon, campaign, and nutrition details through the McDonald's MCP service. It can also help claim account coupons after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a McDonald's account bearer token to a remote MCP endpoint.

Mitigation: Use only tokens the user is comfortable sending to https://mcp.mcd.cn, keep MCD_TOKEN out of shared logs, and avoid overriding MCD_MCP_URL unless the endpoint is trusted.

Risk: The coupon claim action can modify the user's account by claiming coupons.

Mitigation: Ask for explicit confirmation before running auto-bind-coupons or any one-click coupon claim action.

Risk: The server security verdict is suspicious because the skill combines remote token use with account-changing behavior.

Mitigation: Review the skill before installation and limit use to the documented coupon, campaign, nutrition, time, and store-query workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmwalkercao/skills/mymcdonald)
- [McDonald's MCP service](https://mcp.mcd.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON-RPC responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May present coupon and nutrition results as tables or lists.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
