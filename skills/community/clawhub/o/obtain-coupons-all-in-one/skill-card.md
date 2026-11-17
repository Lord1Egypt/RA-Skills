## Description:

Fetches takeout, courier, travel, and movie-ticket coupons and presents redemption links, codes, or QR codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moooai](https://clawhub.ai/user/moooai)

### License/Terms of Use:

MIT-0

## Use Case:

People using China-market services can ask an assistant to find available takeout, parcel, travel, and movie-ticket coupons and get the links or codes needed to redeem them.

### Deployment Geography for Use:

China-market services; availability depends on the platform.

## Known Risks and Mitigations:

Risk: A persistent install identifier is sent to the coupon service for attribution on requests.

Mitigation: Review this attribution behavior before installing; do not run the skill if persistent identification is unacceptable.

Risk: Third-party coupon links and QR codes lead to external redemption flows with limited privacy detail.

Mitigation: Check link destinations and redemption terms before opening or sharing them; use only if comfortable with China-market and WeChat-style flows.

## Reference(s):

- [Coupon API documentation](references/api_documentation.md)
- [Project homepage (listed in ClawHub metadata)](https://github.com/moooai/obtain-coupons-all-in-one)
- [ClawHub skill release](https://clawhub.ai/moooai/skills/obtain-coupons-all-in-one)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown coupon listings with links, redemption codes, and QR image URLs; optional JSON from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redemption codes should be preserved exactly as returned.]

## Skill Version(s):

2.0.2 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
