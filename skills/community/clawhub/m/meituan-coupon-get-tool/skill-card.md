## Description:

Meituan coupon assistant for claiming eligible coupons across food delivery, dining, hotels, travel, entertainment, retail, and pharmacy categories, checking claim history, and guiding Meituan account authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituan-zhengchang](https://clawhub.ai/user/meituan-zhengchang)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a Meituan account use this skill to claim eligible Meituan coupons, review previous coupon claims and validity periods, and optionally configure recurring daily coupon claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Meituan login tokens, device state, and local coupon history.

Mitigation: Install only from a trusted publisher, use it in a private environment, and avoid contexts where command output, process arguments, or local cache files may be logged or shared.

Risk: The bundled cache and credential CLI is broader than the coupon-claiming purpose.

Mitigation: Review or disable the cache and credential CLI before deployment in environments with other skills or shared workspaces.

Risk: Optional daily automation can claim coupons without further per-run confirmation once enabled.

Mitigation: Enable recurring claims only after explicit user consent and periodically review or disable scheduled jobs when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meituan-zhengchang/skills/meituan-coupon-get-tool)
- [Authentication flow](references/auth-flow.md)
- [Response copy](references/response-copy.md)
- [Recurring claim rules](references/cron-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON-backed command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses concise user-facing coupon status, authentication, claim-history, and recurring-claim messages.]

## Skill Version(s):

1.0.18 (source: server release metadata; artifact frontmatter version 1.0.35)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
