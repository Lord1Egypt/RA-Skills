## Description:

Discover and compare the same product across multiple countries and source types (official stores, marketplaces, retailers) using Brave and/or Tavily web search, then normalize all offers to USD for ranking and spread analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsjwong](https://clawhub.ai/user/wsjwong)

### License/Terms of Use:


## Use Case:

External users, developers, and purchasing analysts use this skill to discover candidate product listings across markets, collect verified offers, and compare same-variant prices after USD normalization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discovery queries can send product names, purchasing plans, or internal identifiers to Brave or Tavily.

Mitigation: Use public or non-sensitive product search terms unless third-party search disclosure is acceptable, and keep API keys in the local environment.

Risk: Price comparisons can be misleading when offers differ by model variant, tax and shipping basis, coupon treatment, condition, seller quality, or warranty coverage.

Mitigation: Confirm the same product variant, normalize the price basis, separate new/refurbished/used listings, check marketplace seller quality, and keep URL plus timestamp evidence.

## Reference(s):

- [Data Shape and Source Type Guide](references/data-shape-and-source-types.md)
- [Global Price Comparison Skill Page](https://clawhub.ai/wsjwong/skills/global-price-comparison)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, or CSV generated from command output and offer CSV inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create an offer CSV template, discover candidate URLs, and write comparison results to a requested output file.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
