## Description:

Shopify Storefront (shopify.com). Use this skill for ANY Shopify Storefront request — reading, creating, and updating data. Whenever a task involves Shopify Storefront, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Store owners and operators use this skill to inspect products, collections, shop metadata, and carts, and to create carts or add merchandise lines through their connected Shopify Storefront.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing-tool setup runs downloaded CLI installation software without requesting installation approval; the remote installer was not inspected, and no malicious behavior was established.

Mitigation: Review and separately approve CLI installation, use a vetted release with integrity verification, and consider disabling automatic skill synchronization.

Risk: Creating carts or adding merchandise lines changes Shopify cart state.

Mitigation: Inspect the live action schema and confirm the exact payload and effect with the user before running a write action.

## Reference(s):

- [Shopify Storefront API documentation](https://shopify.dev/docs/api/storefront/latest)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON request payloads and response data, plus Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads retrieve Shopify Storefront data; cart creation and line additions change cart state and require user confirmation.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
