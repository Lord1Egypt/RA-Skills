## Description:

Generate images by customizing a URL. Drop the URL into websites, presentations, PDFs, or anywhere that loads images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jverlee](https://clawhub.ai/user/jverlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content creators use this skill to create image URLs from prompts and embed generated images in websites, Markdown, presentations, PDFs, CSS, or other surfaces that load image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt text and optional API keys are placed in shareable URLs.

Mitigation: Avoid putting secrets, personal data, confidential business details, or reusable API keys in prompts or image URLs; use anonymous access or a backend-held key for public or shared embeds.

Risk: Generated images are fetched from an external service.

Mitigation: Install and use the skill only when sending prompt text to imglink.ai is acceptable for the intended workflow.

## Reference(s):

- [ImgLink service](https://imglink.ai)
- [ImgLink ClawHub release](https://clawhub.ai/jverlee/skills/imglink)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with image URL examples and HTML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces URLs for generated images; first requests may take longer while the image is generated, and later requests use the cached image.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
