## Description:

Meituan Coupon Bot helps users search Meituan dine-in and delivery coupons, compare listed offers, browse popular coupon lists, and generate purchase links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josssong](https://clawhub.ai/user/josssong)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to find Meituan coupons for dine-in meals and delivery, review coupon prices and sales information, and open purchase links for selected offers.

### Deployment Geography for Use:

China (Meituan-supported cities)

## Known Risks and Mitigations:

Risk: The release evidence reports bundled live-looking API credentials.

Mitigation: Remove or rotate bundled credentials and require secrets to be supplied through a controlled runtime configuration before installation.

Risk: The release evidence reports purchase links that may carry referral or CPS attribution.

Mitigation: Clearly disclose affiliate/referral behavior and the external data sent to Meituan during coupon searches before users open purchase links.

Risk: The skill contacts Meituan services to search coupons and generate links.

Mitigation: Review network use and data-sharing expectations before deployment, especially for user-provided keywords, cities, and location-like parameters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josssong/skills/meituan-coupon-bot)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown coupon summaries with purchase links, plus JSON command results from the local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include Meituan offer links, prices, sales counts, store availability, and product images.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
