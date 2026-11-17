## Description:

A Meituan coupon and ordering assistant that helps users find nearby dining deals, claim coupons, compare product options, and initiate orders in conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituan-union](https://clawhub.ai/user/meituan-union)

### License/Terms of Use:

MIT-0

## Use Case:

External Meituan users use this skill through an agent to claim coupons, search nearby dining group-buy products, review options, and start order flows without switching applications.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: The skill can access a Meituan account, use location-based search, and mutate account state by claiming coupons or starting order flows.

Mitigation: Use it only with an account and environment approved for this commerce workflow, and require explicit user confirmation before coupon or order actions.

Risk: Security evidence flags hidden background execution, host fingerprinting, obfuscated CLIGuard code, and a background updater.

Mitigation: Review the publisher, run the skill only in non-sensitive agent environments, and deploy it only when background execution and updater behavior are documented and controllable.

Risk: The skill uses broad triggers, shortened promotional links, and persistent location authorization.

Mitigation: Keep user consent visible, avoid permanent location authorization unless required, and inspect destination links before presenting or opening them.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/meituan-union/skills/meituan-coupon-order-assistant)
- [Publisher profile](https://clawhub.ai/user/meituan-union)
- [Skill service terms](artifact/references/terms-of-service.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with links, QR-code images, and JSON-parsed command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate account authorization, coupon claims, location-based search, and order creation through local scripts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
