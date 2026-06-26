## Description: <br>
Helps an agent guide Meituan account authentication, claim Meituan coupons, query coupon-claim history, and optionally configure daily automatic coupon claiming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-zhengchang](https://clawhub.ai/user/meituan-zhengchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill through an agent to authenticate a Meituan account, claim available coupons across supported Meituan service categories, review past coupon-claim records, and optionally set a daily automatic claim schedule. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Meituan phone/SMS login and stores reusable account tokens and a device identifier on disk. <br>
Mitigation: Install only from a trusted publisher, require user-initiated login, keep credentials local, and clear login or device data when no longer needed. <br>
Risk: Daily automatic coupon claiming can continue acting in the background after setup. <br>
Mitigation: Enable scheduling only with explicit user consent and provide a clear path to inspect, change, or disable the scheduled task. <br>
Risk: The skill text claims official Meituan status, but the release evidence does not corroborate that claim through publisher metadata. <br>
Mitigation: Represent the release as third-party-owned by the server-resolved publisher handle and verify the publisher before entering account credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meituan-zhengchang/meituan-coupon-get-tool) <br>
- [Authentication flow reference](references/auth-flow.md) <br>
- [Automatic coupon-claim scheduling rules](references/cron-rules.md) <br>
- [Response copy templates](references/response-copy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with shell commands and JSON script responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local authentication, device, coupon-history, and scheduling state while executing the coupon workflow.] <br>

## Skill Version(s): <br>
1.0.18 (source: release evidence; artifact frontmatter reports 1.0.35) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
