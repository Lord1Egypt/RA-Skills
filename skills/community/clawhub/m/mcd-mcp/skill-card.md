## Description:

麦当劳MCP接口自动化工具，支持自动领券、查询门店库存、计算最优优惠组合、一键下单，解决麦当劳优惠券手动领取麻烦、库存查询不便的问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[winter1102](https://clawhub.ai/user/winter1102)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to automate McDonald's coupon collection, store inventory lookup, discount calculation, and pickup order workflows through command-line/API automation.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill automates a real McDonald's account and can affect coupons, orders, and purchases.

Mitigation: Review commands before execution and add explicit confirmation and price-review checks before any order placement.

Risk: MCD_TOKEN grants account access and is shown in shell and cron examples.

Mitigation: Treat MCD_TOKEN like a password, avoid embedding it directly in cron or shared scripts, and rotate it if exposed.

Risk: Automated API calls may trigger service risk controls or account restrictions.

Mitigation: Keep call rates within documented limits and stop automation if access is restricted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/winter1102/skills/mcd-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and MCD_TOKEN; account-impacting actions should be reviewed before execution.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
