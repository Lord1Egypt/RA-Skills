## Description:

Coaches on coupon rules and spending decisions with verification checklists, without endorsing platforms or inventing price claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujycode](https://clawhub.ai/user/liujycode)

### License/Terms of Use:

MIT

## Use Case:

Consumers use the skill to find current coupons for food delivery, drinks, hotels, travel, and shopping, and receive claim links or Taobao coupon codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that credentials may be distributed with the skill.

Mitigation: Treat bundled credentials as exposed; the publisher should rotate them, and users should verify they are removed before deployment.

Risk: Search terms may leave the assistant environment without clear disclosure and may travel over unencrypted HTTP; searches may also begin without clear coupon-seeking intent.

Mitigation: Require clear coupon-seeking intent, disclose that search terms are sent externally, and use HTTPS for searches.

Risk: The security review was incomplete: 7 of 8 components were analyzed, and one referenced image was not fully inspectable.

Mitigation: Review the uninspected component before deployment.

## Reference(s):

- [ClawHub life-coupon-expert release](https://clawhub.ai/liujycode/skills/life-coupon-expert)

## Skill Output:

**Output Type(s):** [Text, Markdown, Coupon links, Taobao coupon codes, Guidance]

**Output Format:** [Concise Markdown with claim links, coupon details, and occasional Taobao coupon codes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No fixed post-processing; coupon availability can change and should be checked on the linked platform.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
