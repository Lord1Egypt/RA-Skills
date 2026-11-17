## Description:

Generates and edits images with the GPT-image-2 model through ShiyunApi, supporting text-to-image, image editing, inpainting, background replacement, and multi-image composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gl894761214](https://clawhub.ai/user/gl894761214)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create new images from prompts or edit existing images through ShiyunApi, including posters, avatars, product images, background changes, localized repainting, and multi-image composition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and edited images are sent to ShiyunApi for processing.

Mitigation: Use the skill only when sharing the prompt and input images with ShiyunApi is acceptable.

Risk: The helper can persist SHIYUN_API_KEY in the user's shell or user environment.

Mitigation: Prefer setting SHIYUN_API_KEY manually for the current session, or use process-only storage when persistence is not required.

Risk: Image URLs returned by the API are downloaded automatically.

Mitigation: Review downloaded files before opening, sharing, or using them in downstream workflows.

## Reference(s):

- [ShiyunApi GPT-Image-2 API Reference](artifact/references/api_docs.md)
- [ShiyunApi GPT-Image-2 Examples](artifact/references/examples.md)
- [ShiyunApi GPT-Image-2 Troubleshooting](artifact/references/troubles.md)
- [ShiyunApi text-to-image API](https://shiyunapi.apifox.cn/api-448504710)
- [ShiyunApi image editing API](https://shiyunapi.apifox.cn/api-448504709)
- [ClawHub skill page](https://clawhub.ai/gl894761214/skills/gpt-image-2-shiyunapi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; generated image files, response JSON, and metadata JSON from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include PNG, JPEG, or WebP images, raw response JSON for troubleshooting, and metadata describing saved files and API status.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
