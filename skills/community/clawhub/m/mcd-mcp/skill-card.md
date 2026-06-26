## Description: <br>
麦当劳MCP接口自动化工具，支持自动领券、查询门店库存、计算最优优惠组合、一键下单，解决麦当劳优惠券手动领取麻烦、库存查询不便的问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[winter1102](https://clawhub.ai/user/winter1102) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to automate McDonald's coupon, store inventory, price calculation, and order-related workflows through shell commands that call McDonald's account APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCD_TOKEN can act on the user's McDonald's account. <br>
Mitigation: Keep the token out of shell history, scripts, screenshots, shared terminals, and scheduled jobs unless the exposure has been reviewed. <br>
Risk: Coupon, price, store, item, or order actions may affect real account state or charges. <br>
Mitigation: Require a manual review of store, items, coupons, price, and final charge before any order-related action. <br>
Risk: Automated or scheduled runs can repeat account actions without enough confirmation boundaries. <br>
Mitigation: Use scheduled execution only after reviewing the account token scope, target action, and expected account impact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/winter1102/mcd-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/winter1102) <br>
- [McDonald's MCP endpoint](https://mcp.mcd.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and an MCD_TOKEN environment variable.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
