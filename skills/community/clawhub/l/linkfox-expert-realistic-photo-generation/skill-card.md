## Description:

Generates realistic product-in-hand photos by analyzing product and inspiration images, creating a structured JSON prompt, and using LinkFox image generation to preserve photographic style and role consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn product images and aesthetic references into realistic lifestyle photos of a person holding the product. It supports product-photo ideation, prompt analysis, image generation, and iterative style adjustment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images, prompts, reference images, search terms, and credentials may be sent through LinkFox services.

Mitigation: Use the skill only in trusted environments and avoid submitting sensitive or confidential inputs unless LinkFox service handling is acceptable.

Risk: Selected local files may be uploaded as public URLs.

Mitigation: Confirm files are appropriate to publish before upload and remove or replace any private content before generation.

Risk: The security summary flags paid external calls and automatic feedback reporting.

Mitigation: Confirm expected costs and account configuration before use, and keep LinkFox endpoint environment variables pointed at official HTTPS hosts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-realistic-photo-generation)
- [AI Image Generation API Reference](artifact/skills/linkfox-aigc-imagegen/references/api.md)
- [AI Text Generation API Reference](artifact/skills/linkfox-aigc-textgen/references/api.md)
- [File Upload API Reference](artifact/skills/linkfox-file-upload/references/api.md)
- [Pinterest Image Finder Skill](artifact/skills/pinterest-image-finder/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown responses with structured JSON prompt summaries and inline generated image file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved as local files; selected local files may be uploaded to public HTTPS URLs for downstream generation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
