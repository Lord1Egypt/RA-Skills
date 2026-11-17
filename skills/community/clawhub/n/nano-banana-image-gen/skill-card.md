## Description:

Generate and edit images using Pixwith API's Nano Banana 2 model, supporting text-to-image and image-to-image workflows with up to 4 reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tate-kt](https://clawhub.ai/user/tate-kt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to guide Pixwith image generation and photo editing tasks, including checking credits, uploading allowed reference images, creating tasks, polling results, and returning generated image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected images may be sent to Pixwith and upload storage.

Mitigation: Use the skill only when the user accepts that transfer, and avoid sensitive or private photos unless that transfer is acceptable.

Risk: PIXWITH_API_KEY is a paid-service credential.

Mitigation: Store it only in the intended agent configuration or environment and avoid exposing it in logs, prompts, or shared files.

Risk: Prompt text and opaque API response values can be mishandled when inserted into shell examples.

Mitigation: Build request JSON with a serializer where possible, and preserve API values such as task_id, upload_url, fields, image_url, and result_urls exactly as returned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tate-kt/skills/nano-banana-image-gen)
- [Pixwith homepage](https://pixwith.ai)
- [Pixwith API](https://pixwith.ai/api)
- [Pixwith pricing](https://pixwith.ai/pricing)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown guidance with JSON and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PIXWITH_API_KEY; returns Pixwith task status and result URLs exactly as provided by the API.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
