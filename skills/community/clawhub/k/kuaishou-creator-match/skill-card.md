## Description:

Filter Kuaishou creators by keyword, likes, category, and market to prioritize partnership candidates using engagement and content performance; supports video search, public creator-post retrieval, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Marketing teams and creator partnership researchers can search Kuaishou videos, review a creator's public posts, and inspect video comments to identify and prioritize potential collaborators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and supplied links are sent to a third-party data service, and inspection was partial.

Mitigation: Avoid sending confidential research inputs; review the service's data practices and referenced scripts before use.

## Reference(s):

- [Service access and account information](https://www.guaikei.com)
- [CLI options](artifact/references/options.md)
- [Output envelope schema](artifact/assets/output_envelope.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON result envelopes with agent-readable summaries and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each request returns a result envelope for video search, creator posts, or comments; available fields vary by request.]

## Skill Version(s):

1.1.2 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
