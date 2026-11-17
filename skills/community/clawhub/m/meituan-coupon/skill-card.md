## Description:

Meituan Coupon Assistant helps users authenticate with Meituan, claim coupons across supported Meituan categories, and query previous coupon-claim records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituan-openplatform](https://clawhub.ai/user/meituan-openplatform)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to claim Meituan coupons for food delivery, dining, hotels, tickets, local services, instant retail, medicine, and entertainment, then check the status and validity period of prior claims. The workflow requires Meituan account authentication before coupon issuance or history lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Meituan login credentials and can persist tokens across sessions, including in general agent memory.

Mitigation: Install only when the publisher is trusted, review credential storage before use, and disable or audit the memory-token fallback on shared or cloud agent hosts.

Risk: The skill can create recurring coupon jobs that continue after the initial interaction.

Mitigation: Require explicit user opt-in for scheduling, verify the created job and removal path, and periodically review active cron jobs.

Risk: Server security evidence reports unsafe local file and command-handling code.

Mitigation: Run the skill in an isolated, trusted environment and review shared cache access and command execution paths before deployment.

## Reference(s):

- [Authentication Flow](references/auth-flow.md)
- [Scheduled Coupon Rules](references/cron-rules.md)
- [Response Copy Templates](references/response-copy.md)
- [ClawHub Skill Page](https://clawhub.ai/meituan-openplatform/skills/meituan-coupon)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with coupon tables, plus JSON script results and shell commands for authentication, coupon issuance, history lookup, and scheduling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Beijing time for date-sensitive coupon operations and may maintain local account, device, coupon-history, and schedule state.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
