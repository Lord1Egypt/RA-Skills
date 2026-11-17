## Description:

Lets an agent search and read SellerSpace data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

SellerSpace account holders and agents use it to search and review authorized Amazon store, product, advertising, and shipment data through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unchecked downloads or install additional persistent agent instructions.

Mitigation: Review setup first, install a verified oo CLI release yourself, disable startup skill synchronization when appropriate, and approve any additional skills before installation.

Risk: OOMOL mediates access to SellerSpace, while installer contents and server-side read restrictions have not been verified.

Mitigation: Use minimally scoped SellerSpace credentials and review the access and data associated with each action.

## Reference(s):

- [SellerSpace](https://www.sellerspace.com/)
- [SellerSpace API documentation](https://www.sellerspace.com/help/doc/sellerspace-mcp-configuration-tutorial/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON query results with text summaries]

**Output Parameters:** [Varies by action and query]

**Other Properties Related to Output:** [Results depend on the selected SellerSpace action, connected account permissions, and requested filters.]

## Skill Version(s):

1.0.4 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
