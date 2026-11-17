## Description:

Shopify store management through OpenClaw Commerce API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devkrutik](https://clawhub.ai/user/devkrutik)

### License/Terms of Use:


## Use Case:

Shopify merchants and their agents use this skill to manage store data through OpenClaw Commerce, including orders, products, customers, collections, catalogs, and discounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a powerful OpenClaw Commerce API key for live Shopify administration.

Mitigation: Use a revocable, least-privilege key stored through a protected secret mechanism, and do not paste credentials into chat.

Risk: Create, update, delete, retry, or bulk operations can change live store records.

Mitigation: Confirm exact records, counts, and intended business impact before execution; avoid bulk actions unless they are tightly scoped.

Risk: Customer data and customer secrets may be exposed through unsafe workflows.

Mitigation: Minimize customer data shared with the agent and never provide customer passwords.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/devkrutik/skills/openclaw-commerce-shopify)
- [OpenClaw Commerce](https://openclawcommerce.com)
- [OpenClaw Commerce API Base](https://app.openclawcommerce.com/api/v1)
- [Shopify Admin GraphQL API](https://shopify.dev/docs/api/admin-graphql)
- [Shopify GraphQL Admin API Rate Limits](https://shopify.dev/docs/api/usage/rate-limits)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples, GraphQL request templates, and business-facing text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENCLAW_COMMERCE_API_KEY and confirmation before create, update, or delete operations.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
