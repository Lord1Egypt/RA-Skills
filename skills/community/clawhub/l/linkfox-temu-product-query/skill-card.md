## Description:

Queries Temu products through LinkFox using keyword, product or store ID, category, price, rating, review, sales, listing-date, fulfillment, region, and tag filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce analysts, and agents use this skill to search and compare Temu products by sales, rating, price, category, fulfillment mode, and listing metadata. It also guides LinkFox authentication and billing recovery when the query service cannot be used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Temu research queries and authorization credentials to LinkFox services.

Mitigation: Install only when LinkFox is trusted for the intended search data and use a scoped LinkFox API key where possible.

Risk: Custom LINKFOX_* endpoint overrides could redirect requests away from the expected LinkFox hosts.

Mitigation: Allow endpoint overrides only for trusted HTTPS LinkFox hosts and review environment variables before use.

Risk: Authentication and billing recovery can involve OTPs, API keys, plan selection, and payment order details.

Mitigation: Keep OTPs and API keys out of shared logs, verify plans and payment methods before ordering, and rotate any key that may have been exposed.

Risk: Full product-query responses may be cached or written to local linkfox session files.

Mitigation: Review or delete local cache and session files after sensitive searches.

## Reference(s):

- [Temu Product Query API Reference](references/api.md)
- [LinkFox Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-product-query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON/API result summaries; full product-query responses may be saved as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The query helper caches responses for up to 24 hours and writes full LinkFox API responses under a local linkfox session directory.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
