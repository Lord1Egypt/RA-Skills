## Description:

Fetches takeout coupons for Meituan, Taobao Flash/Ele.me, and JD.com, with redemption codes, instructions, and links to coupon pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moooai](https://clawhub.ai/user/moooai)

### License/Terms of Use:

MIT-0

## Use Case:

People looking for takeout discounts use this skill to find platform-specific coupons and follow instructions to redeem them in the corresponding apps or coupon pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The coupon service receives a persistent anonymous install identifier for attribution.

Mitigation: Use only if comfortable with this attribution; delete scripts/.install_id to reset the local identifier.

Risk: Coupon links and QR codes lead to third-party commercial redemption pages.

Mitigation: Verify the destination and offer details before ordering or sharing payment information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moooai/skills/takeout-coupon)
- [Publisher-listed project homepage](https://github.com/moooai/takeout-coupon)
- [Takeout coupon API documentation](artifact/references/api_documentation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Platform-grouped coupon descriptions, codes, redemption instructions, and links or QR-code image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coupon codes are reproduced exactly as returned by the coupon service.]

## Skill Version(s):

2.0.2 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
