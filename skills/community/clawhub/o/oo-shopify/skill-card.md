## Description:

Use an OOMOL-connected Shopify account to read, create, update, and delete Shopify data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopify users can use the skill through their connected OOMOL account to inspect and manage store data, including products, orders, customers, inventory, and content. The skill uses the oo CLI to run the selected Shopify action and return its result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rated this skill suspicious because setup runs an unpinned external script and scan coverage was incomplete.

Mitigation: Verify the CLI and installer through a trusted source before installing, and review the installer before running it.

## Reference(s):

- [Shopify homepage](https://www.shopify.com)
- [Shopify Admin REST API documentation](https://shopify.dev/docs/api/admin-rest)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub listing](https://clawhub.ai/oomol/skills/oo-shopify)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON action results with Markdown guidance and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by Shopify action and may include records, operation status, or errors.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
