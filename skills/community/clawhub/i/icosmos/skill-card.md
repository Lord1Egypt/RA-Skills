## Description:

Provides Shopify store operations and diagnostics by syncing store domains and tokens from Supabase, running store, theme, product, checkout, and metrics checks, and publishing Shopify blog posts as the only write action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taceywong](https://clawhub.ai/user/taceywong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ecommerce operators use this skill to inspect Shopify store setup, products, checkout flow, orders, blogs, and metrics, then receive diagnostics or command guidance for operational follow-up. The skill can also publish Shopify blog posts when the user explicitly confirms the write action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires sensitive Shopify and Supabase credentials and a local executable whose behavior was not verified by the scan.

Mitigation: Install only from a trusted source, use least-privilege credentials, confirm the target store, and verify local token cache protection and removal.

Risk: Blog publishing is a real write action even though the skill requires a --confirm flag.

Mitigation: Review the content, store domain, blog ID, and confirmation flag before running any publish command.

## Reference(s):

- [Shopify GraphQL Admin API reference](https://shopify.dev/docs/api/admin-graphql/latest)
- [Shopify REST Admin API reference](https://shopify.dev/docs/api/admin-rest/latest)
- [Shopify Storefront API reference](https://shopify.dev/docs/api/storefront/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with command examples and JSON output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends JSON output for command results and omits or masks sensitive fields in outputs.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
