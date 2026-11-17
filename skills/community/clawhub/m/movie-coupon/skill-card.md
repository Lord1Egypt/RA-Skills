## Description:

Helps users find movie-ticket coupons and provides redemption links or QR code image links with instructions for claiming them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moooai](https://clawhub.ai/user/moooai)

### License/Terms of Use:

MIT-0

## Use Case:

Moviegoers can request available ticket discounts and receive coupon links, QR code image links, and redemption guidance for Chinese movie-ticket platforms.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Running the helper sends a persistent anonymous install identifier to the coupon service for attribution, without a clear opt-out.

Mitigation: Review this tracking behavior before installing or running the helper; avoid running it if persistent attribution is unacceptable.

Risk: Returned coupon links and QR codes lead to third-party destinations and a WeChat-based redemption flow.

Mitigation: Inspect destinations and only open links or scan QR codes when you trust the coupon provider and redemption flow.

## Reference(s):

- [ClawHub movie-coupon release](https://clawhub.ai/moooai/skills/movie-coupon)
- [Publisher-provided project homepage (not verified provenance)](https://github.com/moooai/movie-coupon)
- [Movie coupon API documentation](references/api_documentation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with coupon links and QR code image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coupon titles and redemption instructions; availability and destinations depend on the coupon provider.]

## Skill Version(s):

2.0.2 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
