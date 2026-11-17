## Description:

Generates MiniMax videos from text prompts, image references, start and end frames, or subject images using the MiniMax-Hailuo-2.3 API and can download MP4 outputs locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silingyuan0](https://clawhub.ai/user/silingyuan0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to submit MiniMax video generation jobs, check job status, wait for completion, and download generated MP4 files. It supports text-to-video, image-to-video, frame-to-frame, and subject-reference video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and generation metadata are sent to MiniMax using the user's API key.

Mitigation: Review inputs for sensitive data before submission and configure MINIMAX_REGION intentionally for the intended MiniMax endpoint.

Risk: Generated videos can be written to local disk at the requested output path.

Mitigation: Choose output paths deliberately and avoid overwriting important local files.

## Reference(s):

- [MiniMax Video API reference](artifact/references/api.md)
- [ClawHub skill page](https://clawhub.ai/silingyuan0/skills/minimax-video-generate)
- [MiniMax API endpoint for China region](https://api.minimaxi.com/v1)
- [MiniMax API endpoint for international region](https://api.minimax.io/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python command examples; generated videos are saved as MP4 files when downloaded.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and optional MINIMAX_REGION; asynchronous generation returns task status and download information.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
