## Description:

This skill helps agents operate and diagnose Shopify stores by syncing store domains and tokens from Supabase, auditing themes, products, checkout, and metrics, and publishing Shopify blog posts only when explicitly confirmed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taceywong](https://clawhub.ai/user/taceywong)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and store operators use this skill to audit Shopify store setup, products, checkout behavior, and operating metrics, and to publish traffic-building blog posts when an explicit confirmation flag is supplied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable account credentials and cached Shopify tokens could expose store access if local environment variables or cache files are compromised.

Mitigation: Use scoped or short-lived credentials where possible, restrict token permissions, avoid persistent system-wide password environment variables, and rotate or revoke Shopify tokens after suspected exposure.

Risk: The required icosmos-shopify CLI is not included in the artifact evidence and was not reviewed by the security scan.

Mitigation: Review the CLI source, installation path, credential storage behavior, and network destinations before using the skill with production Shopify stores.

Risk: The blog publishing path is a write action that can change a Shopify store's public content.

Mitigation: Require explicit operator approval for publish commands, keep dry-run behavior unless confirmation is present, and validate title, body, store, and blog ID before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taceywong/skills/icosmos-amazon)
- [Shopify GraphQL Admin API reference](https://shopify.dev/docs/api/admin-graphql/latest)
- [Shopify REST Admin API reference](https://shopify.dev/docs/api/admin-rest/latest)
- [Shopify Storefront API reference](https://shopify.dev/docs/api/storefront/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands favor JSON output; sensitive Shopify tokens and order email fields are described as masked or omitted by default.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
