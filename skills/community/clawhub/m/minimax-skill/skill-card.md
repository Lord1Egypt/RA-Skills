## Description:

Unified MiniMax media generation skill for Token Plan workflows, covering audio, image, and video generation plus API key setup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nmww](https://clawhub.ai/user/nmww)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate MiniMax audio, images, and videos from a unified command entrypoint. It is also useful when setting up MINIMAX_API_KEY across local, Docker, or CI environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The video workflow can fetch a service-returned download URL from the user's environment without URL validation.

Mitigation: Run the skill in a restricted runtime, avoid sensitive networks, and review or constrain video downloads until URL validation and response-size limits are added.

Risk: Prompts and generated media requests are sent to MiniMax APIs using the user's API key.

Mitigation: Avoid sending secrets, confidential prompts, or regulated data, and prefer temporary API-key configuration for sensitive environments.

## Reference(s):

- [MiniMax Skill Setup](references/setup.md)
- [ClawHub Skill Page](https://clawhub.ai/nmww/skills/minimax-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MP3 audio files, JPEG image files, MP4 video files, and setup guidance depending on the selected mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
