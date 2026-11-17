## Description:

美团出行红包 helps users authenticate with Meituan, claim travel coupons for flight and train scenarios, view coupon claim history, and optionally schedule recurring coupon claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituan-open-platform](https://clawhub.ai/user/meituan-open-platform)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to claim Meituan travel coupons, check previously claimed coupon records, and manage Meituan phone-login state. The skill can also help configure a daily automatic claim reminder or scheduled claim flow when the user opts in.

### Deployment Geography for Use:

Global, with date and scheduling behavior based on Beijing time (UTC+8)

## Known Risks and Mitigations:

Risk: The skill asks users to complete Meituan phone-login and stores local account tokens and device identifiers.

Mitigation: Install only when the user accepts that login posture; keep tokens local, do not expose token strings in chat, and use the logout or clear-device-token flows when access should be removed.

Risk: The skill can enable persistent automatic coupon claims after a successful claim.

Mitigation: Enable auto-claim only after explicit user opt-in, record the scheduled job ID, and confirm that users know how to view, change, or cancel the scheduled job.

Risk: The security scan flags broad promotional flows and overbroad local cache/shared-token capabilities.

Mitigation: Review the skill and bundled cache tooling before deployment, limit installation to trusted environments, and avoid using the shared-token cache for unrelated skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meituan-open-platform/skills/meituan-coupon-traffic)
- [Authentication flow](artifact/references/auth-flow.md)
- [Cron scheduling rules](artifact/references/cron-rules.md)
- [Response copy templates](artifact/references/response-copy.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Configuration]

**Output Format:** [Markdown user responses with shell command snippets and JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces coupon status messages, authentication prompts, scheduled-task instructions, and structured command results.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
