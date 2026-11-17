## Description:

Helps agents operate and diagnose Shopify stores by auditing themes, products, checkout, and metrics, and by publishing Shopify blog posts only when explicitly confirmed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taceywong](https://clawhub.ai/user/taceywong)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators and agent workflows use this skill to inspect Shopify store health, retrieve store content, diagnose conversion and product issues, test checkout flow, monitor metric anomalies, and publish a blog post when a confirmed write action is intended.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide account credentials and cache privileged Shopify store tokens.

Mitigation: Use only after reviewing the release and verifying the icosmos-shopify executable; prefer scoped or short-lived credentials and confirm token cache location, deletion, and rotation procedures.

Risk: Blog publishing is a Shopify write action.

Mitigation: Require the documented --confirm flag, review the title and body before execution, and treat unconfirmed runs as dry-runs.

Risk: Store diagnostics can involve sensitive store, order, or customer data.

Mitigation: Keep sensitive diagnostics out of shared logs, rely on the documented masking behavior, and avoid exporting persistent credentials in system-wide environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taceywong/skills/icosmos-shopify)
- [Publisher profile](https://clawhub.ai/user/taceywong)
- [Shopify GraphQL Admin API reference](https://shopify.dev/docs/api/admin-graphql/latest)
- [Shopify REST Admin API reference](https://shopify.dev/docs/api/admin-rest/latest)
- [Shopify Storefront API reference](https://shopify.dev/docs/api/storefront/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and JSON output conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shopify command outputs are expected to use JSON fields such as store_domain, api_version, meta, and data when available.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
