## Description: <br>
Automates Meituan coupon claiming in an OpenClaw browser session and summarizes claimed coupon counts, total value, and coupon categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayue-oss](https://clawhub.ai/user/ayue-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to open the Meituan coupon page, claim available coupons, read the coupon-detail snapshot, and report the results. It can also guide a daily scheduled reminder for recurring coupon collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a browser session to claim Meituan coupons and those clicks may affect the logged-in account. <br>
Mitigation: Use it only in the intended browser profile, confirm the account before running, and treat the actions as real account activity. <br>
Risk: Daily scheduling can cause recurring coupon-claim attempts without another prompt. <br>
Mitigation: Enable the daily schedule only when recurring automation is desired, and review or disable the schedule if account or coupon preferences change. <br>
Risk: Coupon availability, page state, login requirements, and Meituan page behavior can change. <br>
Mitigation: Check the returned status and coupon summary after execution, and retry manually after login or later when the page reports login, already-claimed, or high-traffic states. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ayue-oss/meituan-coupon-auto) <br>
- [Publisher profile](https://clawhub.ai/user/ayue-oss) <br>
- [Meituan coupon page](https://click.meituan.com/t?t=1&c=2&p=mcB9ObxznZMn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code] <br>
**Output Format:** [Markdown with browser tool calls, JavaScript snippets, JSON schedule configuration, and coupon summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser automation may perform real account actions in the logged-in Meituan session.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
