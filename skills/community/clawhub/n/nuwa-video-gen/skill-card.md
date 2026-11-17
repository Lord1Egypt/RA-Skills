## Description:

Generates videos with the MiniMax Nuwa API from text prompts, image prompts, start and end frames, or subject-reference face images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superluanxu](https://clawhub.ai/user/superluanxu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-creation agents use this skill to submit MiniMax video-generation jobs, poll for completion, and save the generated MP4 file locally for delivery to a user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and supplied image URLs, including face images in subject mode, are sent to MiniMax under its service terms.

Mitigation: Use only authorized, non-sensitive prompts and images, and confirm the user is comfortable with MiniMax processing before generation.

Risk: The script writes a generated video file to a local output path.

Mitigation: Choose the output path deliberately and avoid overwriting important local files.

Risk: The skill depends on Python, requests, and a MiniMax API key in the execution environment.

Mitigation: Use a virtual environment, pin dependencies where possible, and provide MINIMAX_API_KEY only in trusted runtime contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superluanxu/skills/nuwa-video-gen)
- [MiniMax API platform](https://platform.minimaxi.com)
- [MiniMax API documentation](https://platform.minimaxi.com/docs/llms.txt)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [MP4 video file with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the generated video to the requested output path; defaults to output.mp4.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
