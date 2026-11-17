## Description:

Shopify (shopify.com). Use this skill for ANY Shopify request — reading, creating, updating, and deleting data. Whenever a task involves Shopify, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Shopify store operators and developers use the skill to read and manage data in a connected Shopify account. It supports catalog, orders, customers, inventory, content, and other Shopify resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup downloads and runs software without a separate installation approval step.

Mitigation: Review and approve the CLI installation separately, preferably using a fixed release whose integrity you can verify.

Risk: OOMOL handles connector requests and manages the Shopify connection; its remote implementation and installer contents were not verified.

Mitigation: Grant only necessary Shopify permissions, require approval for refunds, publishing, updates, and deletions, and review bundled-skill synchronization before allowing persistent agent changes.

## Reference(s):

- [Shopify Admin API documentation](https://shopify.dev/docs/api/admin-rest)
- [Shopify](https://www.shopify.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [CLI commands with JSON request payloads and concise instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
