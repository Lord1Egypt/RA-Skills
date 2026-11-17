## Description:

Search and read Skio data, including orders, products, storefront users, and subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Teams use the skill to search and read Skio commerce data through their connected account. It covers orders, products, storefront users, and subscriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup may run a remote installer whose contents are not verified.

Mitigation: Inspect the installer, use a verified fixed release, and explicitly approve local changes before enabling setup.

Risk: A connected account may grant broader Skio access than the requested reads require.

Mitigation: Limit Skio permissions to the reads needed and review the CLI's cross-agent skill synchronization settings.

## Reference(s):

- [Skio API documentation](https://help.skio.com/docs/using-the-skio-api)
- [Skio](https://skio.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON data, Text summaries]

**Output Format:** [Structured Skio records returned as JSON, which the agent can summarize in text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only search and listing results; available data depends on the connected account and requested filters.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
