## Description:

Helps agents publish and manage Temu US product listings through LinkFox-supported Partner US product APIs for the V2 add-product flow, category attributes, image upload, listing queries, edits, inventory, and supply-price tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace operators, and developers use this skill to prepare Temu US product listings, look up required category and specification data, upload product images, and maintain listing, inventory, and price data through guided API calls and scripts.

### Deployment Geography for Use:

Global, for Temu US marketplace operations.

## Known Risks and Mitigations:

Risk: The skill handles powerful LinkFox and Temu store credentials.

Mitigation: Use only trusted LinkFox and Temu accounts, avoid printing full access tokens, keep the local token store private, and rotate tokens if exposure is suspected.

Risk: Product, inventory, price, and sensitive-attribute scripts can mutate live marketplace data.

Mitigation: Review each payload, confirm the target store, site, and management type, and prefer read-only query scripts before executing add, update, stock, price, or sensitive-attribute operations.

Risk: Environment-selected gateway variables can redirect network calls.

Mitigation: Clear or audit LINKFOX_* and TEMU_* endpoint override variables before use, especially in shared shells or CI environments.

Risk: Payment, account, or billing-related flows may affect costs or access.

Mitigation: Confirm authorization and billing steps with the user before running scripts or guidance that could create payment orders, consume account resources, or change account state.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-add-product-us)
- [Temu accessToken authorization](references/access-token.md)
- [API reference](references/api.md)
- [Authorization flow](references/authorization-flow.md)
- [Category, attribute, and specification APIs](references/category-spec-apis.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [Partner US product API catalog](references/partner-us-catalog.md)
- [Product edit APIs](references/product-edit-apis.md)
- [Product publish APIs](references/product-publish-apis.md)
- [Product query APIs](references/product-query-apis.md)
- [Stock and price APIs](references/stock-price-apis.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON API responses saved to files or printed as summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts write full responses under a linkfox date/session data directory and print either full JSON for small responses or summaries for larger responses; --inline requests full stdout output.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
