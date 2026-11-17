## Description:

Generate and edit images with Google's Nano Banana Pro (Gemini 3 Pro Image) API, including text-to-image, image-to-image editing, reference-image workflows, and configurable 1K, 2K, or 4K resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

Developers, creators, and agents use this skill to turn image requests into Gemini image-generation or image-editing calls, optionally using input or reference images for editing, style, character, or subject consistency. It is suited for generating image files and prompt guidance from natural-language visual requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input or reference images may be sent to Google for processing.

Mitigation: Use the skill only with images and prompts you are permitted to share with Google, and avoid sensitive or regulated content unless approved.

Risk: API keys can be exposed when passed directly on the command line.

Mitigation: Prefer the GEMINI_API_KEY environment variable over the --api-key argument and avoid logging or sharing command histories that contain secrets.

Risk: The Python script declares broad dependency ranges.

Mitigation: Pin dependencies or run the skill in an isolated environment before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pauldelavallaz/skills/morfeo-nano-banana-pro)
- [Google AI Studio Gemini 3 Pro Image Preview Endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=${API_KEY})
- [Vertex AI Gemini 3 Pro Image Preview Endpoint](https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/publishers/google/models/gemini-3-pro-image-preview:predict)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports 1K, 2K, and 4K image-size options, text-to-image generation, image editing, and reference-image workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
