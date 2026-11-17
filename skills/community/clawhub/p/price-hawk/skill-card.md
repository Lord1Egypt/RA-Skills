## Description:

Compares public Amazon, Walmart, and eBay offers by price, condition, seller, availability, and shipping, including Amazon seller listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and resale researchers use this skill to compare public product offers across stores and distinguish new, refurbished, and used listings before deciding where to buy or how to price an item.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawLink plugin installation and one-time device pairing are required before use.

Mitigation: Review the plugin and approve pairing only for the intended ClawLink account.

Risk: Marketplace lookups consume paid ClawLink credit.

Mitigation: Check the current per-call price and request approval before large batches or higher-cost calls.

Risk: Fuzzy matches, differing item conditions, and changing prices can make comparisons misleading.

Mitigation: Verify the model and condition, compare shipping, and state when prices were retrieved.

## Reference(s):

- [Price Hawk on ClawHub](https://clawhub.ai/hith3sh/skills/price-hawk)
- [ClawLink OpenClaw documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=price-hawk)
- [Verify the ClawLink plugin](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown price comparisons and shopping guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes offer condition, seller, shipping, and retrieval time when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
