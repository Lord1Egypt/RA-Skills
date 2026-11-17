## Description:

Use this skill to read and manage WooCommerce products, orders, customers, coupons, and media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and store operators use a connected WooCommerce account to inspect store data and create or update products, orders, coupons, and related records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs remote installers that were not fully verified, and automatic synchronization can change agent skills.

Mitigation: Review and install the CLI separately; disable automatic skill synchronization if you do not want changes across your agents.

Risk: Write and destructive actions can change WooCommerce store data.

Mitigation: Verify the connected store and account permissions, and retain approval for every store mutation.

## Reference(s):

- [WooCommerce REST API documentation](https://developer.woocommerce.com/docs/apis/rest-api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
