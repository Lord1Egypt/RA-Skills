## Description: <br>
帮助用户领取和查询美团机票、火车票等出行优惠券，并可在用户选择后设置每日自动领券。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-open-platform](https://clawhub.ai/user/meituan-open-platform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users ask the agent to claim Meituan travel coupons, review previous coupon claims, manage login state, or opt into daily automatic coupon claiming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says reusable Meituan login and device tokens are stored locally in shared cache storage. <br>
Mitigation: Install only after verifying the publisher, use the logout and clear-device-token flows when finished, and avoid using the skill on shared or untrusted machines. <br>
Risk: The security evidence says the skill can create recurring automatic coupon-claim jobs. <br>
Mitigation: Enable daily auto-claiming only when recurring account actions are desired, and use the cancel-auto-claim flow when the schedule is no longer needed. <br>
Risk: The security verdict is suspicious and recommends review before entering a phone number or SMS code. <br>
Mitigation: Review the authentication flow and publisher identity before providing phone numbers, SMS codes, or account access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meituan-open-platform/meituan-coupon-traffic) <br>
- [Authentication flow reference](references/auth-flow.md) <br>
- [Scheduled auto-claim rules](references/cron-rules.md) <br>
- [Response copy templates](references/response-copy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown responses with shell command execution guidance and JSON script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger local Python scripts, persist local authentication state, and create scheduled coupon-claim jobs when enabled by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
