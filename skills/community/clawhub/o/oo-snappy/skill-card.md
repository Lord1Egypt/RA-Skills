## Description:

Search Snappy's gift catalog and read account, collection, product, variant, tag, availability, and pricing information through a connected Snappy account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to search Snappy's gift catalog and retrieve details about accounts, collections, products, variants, tags, availability, and pricing through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute an unchecked remote CLI installer and make persistent changes, including changes to other agent skills.

Mitigation: Review and approve CLI installation separately, prefer a reviewed and pinned release, and decide whether bundled-skill synchronization is wanted before setup.

## Reference(s):

- [Snappy homepage](https://www.snappy.com/)
- [Snappy API documentation](https://docs.snappy.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance, oo CLI commands, and JSON action responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action responses may include an execution ID in response metadata.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
