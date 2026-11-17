## Description:

Fetches parcel-shipping coupons and provides redemption links and QR code image links for use with WeChat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moooai](https://clawhub.ai/user/moooai)

### License/Terms of Use:

MIT-0

## Use Case:

People sending parcels use this skill to find shipping offers and receive coupon links or QR codes for redemption in WeChat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent install identifier is sent with coupon lookups and may allow the API operator or coupon providers to correlate requests across runs.

Mitigation: Review this attribution behavior before installing or using the skill if request correlation is unacceptable.

Risk: Coupon links and QR codes lead to external promotional destinations.

Mitigation: Verify destination domains before opening links or scanning codes.

Risk: Broad shipping questions may trigger coupon lookups without a clear request for offers.

Mitigation: Use the skill only for explicit coupon requests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/moooai/skills/parcel-coupon)
- [Project homepage (listed in skill metadata)](https://github.com/moooai/parcel-coupon)
- [Parcel coupon API documentation](references/api_documentation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Formatted coupon details with links and QR code image URLs; optional JSON from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coupon availability and redemption depend on the external service and destinations.]

## Skill Version(s):

2.0.2 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
