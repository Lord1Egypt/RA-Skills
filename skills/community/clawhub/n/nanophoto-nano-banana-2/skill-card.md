## Description:

Generate or edit images with the NanoPhoto.AI Nano Banana 2 API, including text-to-image, image-to-image with public URLs, status checks, and optional Google Search prompt enhancement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanophotohq](https://clawhub.ai/user/nanophotohq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to submit NanoPhoto.AI Nano Banana 2 image generation or editing jobs, poll generation status, and return resulting image URLs and generation details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and public image URLs are sent to the NanoPhoto.AI service and may spend NanoPhoto credits.

Mitigation: Use the skill only for authorized, non-sensitive content and confirm the user intends to use NanoPhoto credits.

Risk: API keys can be exposed if pasted into chat or passed directly on a command line.

Mitigation: Configure NANOPHOTO_API_KEY through the platform's secure environment setting or documented config path, and avoid the --api-key flag unless necessary.

Risk: Edit mode requires public image URLs and does not support local or base64 image uploads.

Mitigation: Ask for public image URLs only, limit edit requests to no more than 14 images, and avoid private or sensitive images.

## Reference(s):

- [Nano Banana 2 API Reference](references/api.md)
- [NanoPhoto.AI Homepage](https://nanophoto.ai)
- [NanoPhoto.AI API Key Settings](https://nanophoto.ai/settings/apikeys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns imageUrl, generationId, progress details, and status/error information when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
