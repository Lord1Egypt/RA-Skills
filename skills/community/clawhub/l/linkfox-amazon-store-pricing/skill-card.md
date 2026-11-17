## Description:

Queries Amazon seller Product Pricing data through LinkFox, including ASIN/SKU prices, competitive pricing, listing and item offers, Featured Offer Expected Price, and competitive summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Amazon sellers use this skill to query Amazon Product Pricing information for individual or batched ASIN and seller SKU workflows. It helps compare offers, inspect Buy Box and Featured Offer signals, and estimate competitive pricing while using LinkFox account and authorization flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Amazon seller pricing data and saves pricing responses to local JSON files.

Mitigation: Install only in workspaces where saved pricing output is acceptable, review the output directory, and treat generated files as sensitive business data.

Risk: Authentication and onboarding flows may involve LinkFox API keys, SMS codes, account login, billing orders, or payment QR files.

Mitigation: Avoid passing secrets in logged command lines, verify account and billing actions before execution, and keep generated payment artifacts private.

Risk: Endpoint override environment variables can redirect requests away from the expected LinkFox service.

Mitigation: Use default endpoints unless the override target is fully trusted and intentionally configured.

Risk: Repeated invalid or high-rate Amazon SP-API calls can trigger temporary store-level protection or throttling.

Mitigation: Follow the documented cooldown and retry guidance, correct bad parameters or authorization issues before retrying, and avoid automatic repeated calls.

## Reference(s):

- [Amazon Store Product Pricing API Reference](artifact/references/api.md)
- [Authentication and Billing Onboarding](artifact/references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-store-pricing)
- [Amazon getPricing](https://developer-docs.amazon.com/sp-api/reference/getpricing)
- [Amazon getCompetitivePricing](https://developer-docs.amazon.com/sp-api/reference/getcompetitivepricing)
- [Amazon getListingOffers](https://developer-docs.amazon.com/sp-api/reference/getlistingoffers)
- [Amazon getItemOffers](https://developer-docs.amazon.com/sp-api/reference/getitemoffers)
- [Amazon getItemOffersBatch](https://developer-docs.amazon.com/sp-api/reference/getitemoffersbatch)
- [Amazon getListingOffersBatch](https://developer-docs.amazon.com/sp-api/reference/getlistingoffersbatch)
- [Amazon getFeaturedOfferExpectedPriceBatch](https://developer-docs.amazon.com/sp-api/reference/getfeaturedofferexpectedpricebatch)
- [Amazon getCompetitiveSummary](https://developer-docs.amazon.com/sp-api/reference/getcompetitivesummary)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON files]

**Output Format:** [Markdown guidance with shell commands and JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full JSON responses under the working directory and may print either full JSON or a summary depending on response size.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
