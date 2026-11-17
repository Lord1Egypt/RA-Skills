## Description:

Generate MiniMax Hailuo videos from text prompts or first and last frame image URLs, then query generation status and download completed videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to submit MiniMax Hailuo video generation jobs, monitor their status, and retrieve generated MP4 files from completed tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and generation metadata are sent to MiniMax using the user's local API key.

Mitigation: Avoid confidential prompts and private or internal image URLs unless sharing them with MiniMax is acceptable for the deployment environment.

Risk: Downloaded videos are written to a user-provided local path.

Mitigation: Use a dedicated output directory and choose paths that cannot overwrite important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongjiahao371-pixel/skills/minimax-video-gen)
- [Publisher profile](https://clawhub.ai/user/hongjiahao371-pixel)
- [MiniMax video generation API endpoint](https://api.minimaxi.com/v1/video_generation)
- [MiniMax video generation query endpoint](https://api.minimaxi.com/v1/query/video_generation)
- [MiniMax file retrieval endpoint](https://api.minimaxi.com/v1/files/retrieve)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls, files]

**Output Format:** [Command-line text with task IDs, file IDs, API responses, and downloaded MP4 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local MiniMax API key; generated download links are time-limited.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
