## Description:

A Shopify operations and diagnostics skill that retrieves store domains and tokens from Supabase, audits theme, product, checkout, and metric issues, and supports confirmed blog publishing as its only write operation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taceywong](https://clawhub.ai/user/taceywong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and commerce teams use this skill to audit Shopify storefront health, product quality, checkout behavior, order and metrics signals, and to publish a Shopify blog post only when explicitly confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account credentials and Shopify tokens may be stored or cached without clear protection, scope, expiration, or deletion controls.

Mitigation: Use least-privilege Shopify scopes, avoid long-lived password environment variables where possible, restrict local cache permissions, and document cache location, expiry, and deletion procedures before use.

Risk: The referenced icosmos-shopify executable lacks server-resolved provenance in the available evidence.

Mitigation: Confirm the executable source and integrity, scan it before installation, and install only in environments authorized for the connected Shopify stores.

Risk: Blog publishing is a write operation that can change live Shopify content.

Mitigation: Keep publishing gated behind explicit confirmation, review generated content before execution, and use dry-run behavior when confirmation is absent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taceywong/skills/icosmos-shop)
- [Shopify GraphQL Admin API reference](https://shopify.dev/docs/api/admin-graphql/latest)
- [Shopify REST Admin API reference](https://shopify.dev/docs/api/admin-rest/latest)
- [Shopify Storefront API reference](https://shopify.dev/docs/api/storefront/latest)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Analysis, Guidance]

**Output Format:** [Markdown guidance with CLI command examples and JSON-oriented command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default command output is documented as JSON with store_domain, api_version, meta, and data fields; paginated responses expose page_info metadata.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
