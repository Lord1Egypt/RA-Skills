## Description:

Converts Chinese image-generation requests into structured English JSON prompts for Nano Banana/Gemini image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xk103295870-alt](https://clawhub.ai/user/xk103295870-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn Chinese descriptions for product images, avatars, logos, posters, and social media visuals into structured JSON prompts for image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated JSON may include logo text, personal likenesses, or safety settings that are unsuitable for the intended image API request.

Mitigation: Review the generated JSON before sending it to an image API, especially text_content, personGeneration, and safetySetting.

Risk: The skill may infer style, color, aspect ratio, or use-case classification from sparse user input.

Mitigation: Ask for clarification or edit inferred fields before using prompts for production assets.

## Reference(s):

- [Nano Banana API documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-1-flash-image)
- [Google AI Studio](https://aistudio.google.com)
- [Prompt example library](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)
- [Nano Banana Prompt Generator examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown containing structured JSON image-generation prompt objects with English prompt fields and Chinese explanation fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes model, prompt, numberOfImages, aspectRatio, outputFormat, safetySetting, and optional text_content fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill document)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
