## Description:

Create high-quality AI images from text prompts with customizable aspect ratios, returned as base64 data URLs for immediate display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarahglassseeen](https://clawhub.ai/user/sarahglassseeen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to generate images from text prompts through Gilotex Image API, including illustrations, posters, thumbnails, and chatbot responses that include images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Gilotex's external image API, which may expose secrets, private personal data, regulated data, or confidential business information.

Mitigation: Avoid including sensitive or confidential information in prompts unless the external service's handling practices are trusted.

Risk: The skill depends on an external image API endpoint for image generation.

Mitigation: Review external service availability, terms, and data handling before using the skill in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sarahglassseeen/skills/image-free)
- [Publisher profile](https://clawhub.ai/user/sarahglassseeen)
- [Gilotex Image API endpoint](https://gilotex.pro.vn/api/image)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with JSON function schema and base64 image data URL responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports prompt, aspect ratio, and optional model parameters; default aspect ratio is 9:16.]

## Skill Version(s):

1.2.0 (source: server release evidence and artifact text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
