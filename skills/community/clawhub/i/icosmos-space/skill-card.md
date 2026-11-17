## Description:

Provides Shopify store operations and diagnostics using Supabase-synced store domains and tokens, with read-only checks for themes, products, checkout, and metrics plus confirmed blog publishing as the only write action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taceywong](https://clawhub.ai/user/taceywong)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Shopify store operators use this skill to retrieve store data, run operational audits, troubleshoot checkout and metrics issues, and publish a blog post only after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill caches high-privilege Shopify store tokens locally without evidence describing the cache location or protection model.

Mitigation: Confirm the token cache path, file permissions, deletion process, and token rotation process before use.

Risk: Environment credentials and cached Shopify tokens may expose sensitive store access if mishandled.

Mitigation: Treat ICOSMOS_USER_EMAIL, ICOSMOS_USER_PASSWORD, and cached tokens as secrets, and use Shopify app scopes with the least privilege needed.

Risk: The blog publishing command is a write action that can modify a Shopify store.

Mitigation: Use --confirm only when the operator intends to publish and has reviewed the target store, blog ID, title, and body file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taceywong/skills/icosmos-space)
- [Shopify GraphQL Admin API reference](https://shopify.dev/docs/api/admin-graphql/latest)
- [Shopify REST Admin API reference](https://shopify.dev/docs/api/admin-rest/latest)
- [Shopify Storefront API reference](https://shopify.dev/docs/api/storefront/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON-oriented command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most operations are read-only; blog publishing requires an explicit --confirm flag.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
