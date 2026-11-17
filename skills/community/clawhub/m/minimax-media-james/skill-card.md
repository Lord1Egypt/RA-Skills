## Description:

Use MiniMax API for image generation and text-to-speech (TTS), supporting the image-01 model for images and speech-2.8-hd for voice synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlin53882](https://clawhub.ai/user/jlin53882)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate images and text-to-speech audio through MiniMax from command-line prompts or text inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and text-to-speech inputs are sent to MiniMax.

Mitigation: Avoid submitting secrets, regulated data, or sensitive personal information unless MiniMax handling is approved for that data.

Risk: MINIMAX_BASE_URL can change the endpoint that receives requests and credentials.

Mitigation: Leave MINIMAX_BASE_URL unset unless the replacement endpoint is fully trusted and reviewed.

Risk: Generated image downloads and temporary output paths are not strongly validated.

Mitigation: Run the skill in a constrained workspace and prefer a revised version that validates download URLs, response sizes, and temporary-file creation.

## Reference(s):

- [MiniMax Platform](https://platform.minimax.io)
- [MiniMax API endpoint](https://api.minimax.io)
- [ClawHub skill page](https://clawhub.ai/jlin53882/skills/minimax-media-james)

## Skill Output:

**Output Type(s):** [Files, JSON, API Calls]

**Output Format:** [JSON with generated image or audio file paths, byte sizes, and related response details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes PNG image files or MP3 audio files locally and requires MINIMAX_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
