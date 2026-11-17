## Description:

Publish and schedule social media posts across LinkedIn, Bluesky, Instagram, TikTok, Pinterest, YouTube Shorts and Mastodon, then verify delivery with per-post receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mertkodzhaaslan](https://clawhub.ai/user/mertkodzhaaslan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to publish, schedule, queue, verify, and manage social media content across connected Postlia accounts. It helps agents handle posting workflows while checking account connections, quotas, media requirements, and delivery receipts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect connected social accounts by posting, scheduling, queueing, deleting scheduled posts, or importing media.

Mitigation: Require the agent to restate the target platforms, content, timing, and media source, then wait for explicit user approval before taking account-affecting actions.

Risk: Posts may fail or publish only partially across selected platforms.

Mitigation: Use Postlia delivery receipts or recent post status and report platform-provided error messages without inventing causes.

Risk: Media-platform posts can be rejected when media or platform-specific options are missing.

Mitigation: Import media into Postlia storage first and confirm required TikTok, Pinterest, or YouTube options before creating the post.

## Reference(s):

- [ClawHub Postlia Skill](https://clawhub.ai/mertkodzhaaslan/skills/postlia)
- [Postlia](https://postlia.com)
- [Postlia REST API](https://postlia.com/api/v1)
- [Postlia MCP Server](https://postlia.com/api/mcp)
- [Postlia Account Settings](https://postlia.com/settings)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline REST examples, JSON payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POSTLIA_API_KEY; account-affecting posting, scheduling, deletion, and media-import actions should be confirmed before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
