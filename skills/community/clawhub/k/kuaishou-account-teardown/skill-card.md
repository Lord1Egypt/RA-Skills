## Description:

Search public Kuaishou videos, retrieve creators’ public posts and video comments, and summarize engagement patterns for account and competitor analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content strategists and social media analysts use the skill to research public Kuaishou creators, compare engagement and posts, and identify content patterns and gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and account or video links are sent to the third-party Guaikei service.

Mitigation: Use non-sensitive search terms and public links, and proceed only if comfortable sharing them with Guaikei.

## Reference(s):

- [Usage options](references/options.md)
- [Version history](references/changelog.md)
- [Output envelope schema](assets/output_envelope.schema.json)
- [Guaikei service and access information](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON envelope with video, creator, or comment results and engagement metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public-data results only; requires a Guaikei API token. Per-plan result limits apply.]

## Skill Version(s):

1.1.1 (source: frontmatter, changelog, package.json; released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
