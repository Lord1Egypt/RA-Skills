## Description:

Upload an image or video to PostLake and attach it to a post. Use when a post needs media, or for platforms that require it (Instagram, TikTok, YouTube, Pinterest).

This skill is ready for commercial/non-commercial use.

## Publisher:

[postlake](https://clawhub.ai/user/postlake)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to upload approved media to PostLake and attach returned media IDs to posts for channels that require images or video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The URL workflow could fetch and re-upload unintended internal or sensitive content.

Mitigation: Prefer explicitly selected local files or trusted HTTPS media sources, and apply size and content-type checks before upload.

Risk: A broad PostLake API key could allow media uploads beyond the intended account or workflow.

Mitigation: Use a scoped POSTLAKE_API_KEY for a trusted PostLake account and review upload targets before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/postlake/skills/postlake-media)
- [PostLake API base URL](https://api.postlake.dev)
- [PostLake media upload endpoint](https://api.postlake.dev/v1/media)
- [PostLake post creation endpoint](https://api.postlake.dev/v1/posts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance expects a scoped POSTLAKE_API_KEY and caller-selected media.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
