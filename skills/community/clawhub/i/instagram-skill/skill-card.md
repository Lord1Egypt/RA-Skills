## Description:

Helps an agent create Instagram posts, check and preview media, and schedule or publish approved posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and social media teams use it to prepare Instagram carousels, images, Reels, and Stories, validate media and captions, and schedule approved posts across one or more accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote service behavior and client credential storage have not been audited.

Mitigation: Use browser sign-in where available, keep API-key URLs and upload-session files private, and connect only intended accounts.

Risk: Content could be published or scheduled to an unintended account or with an unnoticed issue.

Mitigation: Review the complete preview and intended accounts before approving publication.

Risk: Incorrect CSV measurement dates can distort performance rankings.

Mitigation: Verify measurement dates before relying on rankings.

Risk: Media repairs may leave a file that still fails a platform check.

Mitigation: Run the media checker again without --fix after repairs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/social-media-skills/skills/instagram-skill)
- [Instagram platform limits and guidance](artifact/references/instagram-specs.md)
- [Post plan format](artifact/references/plan-json.md)
- [WoopSocial setup and posting guide](artifact/references/woopsocial.md)
- [WoopSocial MCP tools reference](https://docs.woopsocial.com/mcp/tools-reference)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown, JSON]

**Output Format:** [JPEG media, captions, JSON plans and requests, and Markdown previews and schedules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can prepare content for one or multiple Instagram accounts.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
