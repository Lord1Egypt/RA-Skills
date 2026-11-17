## Description:

Routes e-commerce image requests to product image sets, detail-page images, or custom image generation using LinkPix and qhkit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce sellers and their agents use this skill to select an image-generation mode and create product hero images, image sets, detail-page visuals, and custom marketing images from prompts or reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images are uploaded to the image provider during generation.

Mitigation: Use only images the user is comfortable uploading to that provider.

Risk: Image generation can consume account credits.

Mitigation: Check the estimated charge and available balance before generating images.

Risk: The CLI requires an API key and is installed as software.

Mitigation: Protect the API key, use a reviewed pinned qhkit version, and review upgrades before installing them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-ecom-image)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Guidance, Shell commands, Configuration]

**Output Format:** [Generated product images; Markdown guidance and JSON parameters for qhkit commands]

**Output Parameters:** [Varies by image mode; may include a prompt, reference images, model, theme, and image count]

**Other Properties Related to Output:** [Image generation may upload supplied reference images to the provider and consume credits.]

## Skill Version(s):

0.1.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
