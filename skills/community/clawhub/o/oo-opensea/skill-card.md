## Description:

Search and read OpenSea collection, NFT, listing, offer, trait, and account data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to search OpenSea and retrieve collection, NFT, listing, offer, trait, and account information through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructs the agent to execute downloaded installer code without a clear approval or verification step.

Mitigation: Review the setup, install a verified CLI release yourself, or require explicit approval and inspection before the agent runs either installer.

Risk: OpenSea requests pass through an unverified hosted connector using the connected account.

Mitigation: Review the OOMOL connection and the account access it uses before enabling the skill.

## Reference(s):

- [OpenSea API documentation](https://docs.opensea.io/reference/api-overview)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [OpenSea](https://opensea.io)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [JSON query data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented OpenSea results; action inputs follow the live connector schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
