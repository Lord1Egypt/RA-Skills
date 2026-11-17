## Description:

Analyzes batches of social media posts and engagement data to extract structural features, compare top and bottom performers, and generate a data-backed content blueprint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

Apache-2.0

## Use Case:

Content creators, marketers, and social media teams use this skill to analyze their own posts after publication and identify linguistic or structural patterns associated with higher engagement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input posts may contain private drafts, confidential campaign material, or third-party personal data.

Mitigation: Only analyze posts the user is allowed to process, and avoid supplying confidential or sensitive post data unless the environment is approved for it.

Risk: JSON output includes short previews of the input posts.

Mitigation: Review JSON exports before sharing them and redact previews when they could expose private or sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-post-forensics)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain-text report by default, with optional JSON output for pipelines.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The JSON mode includes post-level feature summaries, short text previews, insights, and recommendations.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
