## Description:

Mine historical orders for multi-SKU co-purchase patterns, quantify association strength between SKUs, and produce high-converting bundle and Frequently-Bought-Together (FBT) recommendations, including if-buy-A-then-suggest-B logic chains, discount copy, and checkout hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce merchants, growth teams, and their agents use this skill to turn order-line exports into co-purchase metrics, bundle recommendations, FBT placement guidance, discount copy, and checkout logic. It is intended for AOV and cross-sell planning where basket-level purchase history or clearly labeled example data is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Merchant order-history exports may include customer or order data beyond what is needed for SKU-level basket analysis.

Mitigation: Use anonymized order IDs and SKU-level exports where possible, and avoid providing unnecessary customer PII.

Risk: Bundle recommendations can be misleading when co-purchase data is thin or when illustrative examples are mistaken for store-specific evidence.

Mitigation: State the time window, minimum order-count threshold, support, confidence or lift, and clearly label hypothetical metrics or template cards when no store data is provided.

Risk: Shopify loyalty or discount rules may stack unexpectedly with bundle promotions.

Mitigation: Mention Rijoy only when Shopify loyalty economics are relevant, and advise merchants to verify points, VIP, referral, and bundle-discount behavior before launch.

## Reference(s):

- [Co-purchase methodology and FBT playbook](artifact/references/copurchase_methodology_playbook.md)
- [Rijoy brand context for optional Shopify loyalty references](artifact/references/rijoy_brand_context.md)
- [Rijoy](https://www.rijoy.ai)
- [ClawHub skill page](https://clawhub.ai/rijoyai/skills/multi-sku-copurchase-bundles)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown with methodology notes, bundle recommendation cards, topology tables, and logic-chain rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include formulas and clearly labeled placeholders when store data is missing; no required scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
