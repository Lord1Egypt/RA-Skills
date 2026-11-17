## Description:

Generates ecommerce marketing videos for users and helps them submit video jobs, check progress, and download completed videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lu200852](https://clawhub.ai/user/lu200852)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create ecommerce or product marketing videos, track generation status, and retrieve finished video assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The download flow can save files from remote-provided URLs without enough guardrails.

Mitigation: Use only trusted MCP services, validate download URLs and filenames, prefer scoped download tooling, and require explicit confirmation before writing files locally.

Risk: The skill depends on a configured API key for the remote video service.

Mitigation: Keep VIDEO_API_KEY in the configured secret environment file, restrict file permissions, and avoid logging or echoing the key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lu200852/skills/hilight-video-generate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with task IDs, status summaries, download links, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated video files locally when the user asks to download them.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
