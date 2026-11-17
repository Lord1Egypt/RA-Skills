## Description:

Helps agents manage Shopee cross-border GlobalProduct catalog operations through LinkFox wrappers for 34 Shopee Open Platform GlobalProduct APIs, including category lookup, item creation, publishing, price, and stock updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and e-commerce operators use this skill to manage authorized Shopee merchant global products, SKUs, pricing, stock, size charts, and cross-site publishing workflows. It is intended for agent-assisted Shopee catalog operations that require LinkFox authentication and merchant or shop identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox API keys and Shopee merchant account operations.

Mitigation: Treat API keys and saved response files as sensitive business secrets, keep them in access-controlled workspaces, and remove them when no longer needed.

Risk: The skill can make live catalog changes, including delete, publish, price, stock, and billing-related actions.

Mitigation: Require explicit user confirmation and review request bodies before running mutating or billing commands.

Risk: Custom gateway or login URL environment variables could redirect requests away from expected LinkFox HTTPS endpoints.

Mitigation: Use default LinkFox HTTPS endpoints unless the deployment explicitly pins and verifies an approved endpoint.

Risk: Automatic feedback submission can transmit operational context outside the immediate task flow.

Mitigation: Opt out of or block automatic feedback submission when organizational policy requires prior review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-global-product)
- [LinkFox GlobalProduct API reference](artifact/references/api.md)
- [LinkFox onboarding and billing guide](artifact/references/onboarding.md)
- [Shopee GlobalProduct documentation](https://open.shopee.com/documents/v2/v2.global_product.get_category?module=90&type=1)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Files]

**Output Format:** [Markdown guidance with Python command examples and JSON API responses or summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved under a linkfox session data directory; responses larger than 8 KB may be summarized unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
