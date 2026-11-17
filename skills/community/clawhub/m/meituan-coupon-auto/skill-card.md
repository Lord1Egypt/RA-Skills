## Description:

自动领取美团优惠券，并读取领取后的券数量、总金额和分类明细。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayue-oss](https://clawhub.ai/user/ayue-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to automate claiming Meituan coupons in a browser session and summarize the coupons that were received. It can also provide a recurring daily coupon-claim configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a logged-in Meituan browser session to click coupon-claim controls.

Mitigation: Run it only after the user confirms they want the agent to act in that account session.

Risk: The skill includes recurring daily scheduling behavior without enough disablement guidance.

Mitigation: Confirm the schedule, timezone, and how to list, pause, or delete the scheduled task before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayue-oss/skills/meituan-coupon-auto)
- [Meituan coupon claim URL](https://click.meituan.com/t?t=1&c=2&p=mcB9ObxznZMn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration]

**Output Format:** [Markdown with browser automation snippets and JSON schedule configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes coupon counts, total value, coupon categories, status handling, and optional daily scheduling.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
