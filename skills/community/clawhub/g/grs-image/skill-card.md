## Description:

GrsAI Nano Banana Pro image generation tool that uses the GrsAI API for Chinese-language prompts, interior design renderings, launch posters, design materials, and image-to-image reference workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapleslove](https://clawhub.ai/user/mapleslove)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to generate images through the GrsAI Nano Banana Pro API from text prompts or reference images. It is suited to design visualization tasks such as interior renderings, promotional posters, material studies, and prompt-template-assisted image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user prompts and optional reference images to a third-party GrsAI service.

Mitigation: Avoid submitting confidential prompts or reference images, and use a dedicated low-privilege GrsAI API key.

Risk: The remote API response can direct the script to download an image from a returned URL.

Mitigation: Review before installing and consider URL allowlisting, response size limits, and content-type checks before regular use.

Risk: The script depends on external Python packages and a remote image-generation API.

Mitigation: Install dependencies in a virtual environment and pin dependency versions for repeatable use.

## Reference(s):

- [GrsAI Nano Banana API Documentation](https://grsai.ai/zh/dashboard/documents/nano-banana)
- [Prompt Templates](references/prompts.json)
- [ClawHub Grs Image Skill Page](https://clawhub.ai/mapleslove/skills/grs-image)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, files, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated image files saved to disk]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GrsAI API key; prompts and optional reference images are sent to a third-party API, and generated image URLs may be time-limited.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
