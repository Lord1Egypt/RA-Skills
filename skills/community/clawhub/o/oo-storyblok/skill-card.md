## Description:

Search and read Storyblok spaces, stories, links, datasources, and tags through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Storyblok users can retrieve space metadata and search or read stories, links, datasources, datasource entries, and tags from their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup runs an unverified internet installer without requiring user approval.

Mitigation: Review and explicitly approve CLI installation separately; prefer a reviewed, version-pinned installer with integrity verification.

## Reference(s):

- [Storyblok](https://www.storyblok.com)
- [Storyblok Content Delivery API documentation](https://www.storyblok.com/docs/api/content-delivery/v2)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured Storyblok records in JSON with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected read action and the connected Storyblok account.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
