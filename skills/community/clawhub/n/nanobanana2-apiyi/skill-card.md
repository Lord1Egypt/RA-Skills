## Description:

Generate images via APIYI (Gemini 3.1 Flash Image Preview) from text descriptions, with keyword extraction, prompt restructuring, and direct image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunni123](https://clawhub.ai/user/yunni123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn text descriptions into image prompts, review generated prompt options, and create image files through APIYI after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials can be exposed if passed directly on the command line or shown during debugging.

Mitigation: Use an environment variable or protected configuration for APIYI_API_KEY and avoid --debug-key unless reviewing output locally.

Risk: Prompts and generation settings are sent to the third-party APIYI image API.

Mitigation: Do not include secrets, personal data, or sensitive material in image prompts, and review data-sharing expectations before use.

## Reference(s):

- [APIYI image generation endpoint](https://api.apiyi.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent)
- [ClawHub skill page](https://clawhub.ai/yunni123/skills/nanobanana2-apiyi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON prompt suggestions, and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and APIYI_API_KEY; generated images are saved as local files.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
