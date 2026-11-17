## Description:

Generate AI images with any model using ImageRouter API (requires API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dawe35](https://clawhub.ai/user/dawe35)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to produce curl-based guidance for generating and editing images through ImageRouter's API, including model discovery, text-to-image, image-to-image, mask-based edits, and direct downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected local images, masks, and API-authenticated requests may be sent to ImageRouter.

Mitigation: Avoid uploading confidential images unless the user accepts the provider's handling of them, and strip image metadata when appropriate.

Risk: Direct download examples may consume image URLs returned by the service.

Mitigation: Validate returned image URLs before using a direct download pipeline.

## Reference(s):

- [ClawHub ImageRouter skill](https://clawhub.ai/dawe35/skills/image-router)
- [ImageRouter homepage](https://imagerouter.io)
- [ImageRouter model catalog](https://imagerouter.io/models)
- [ImageRouter API keys](https://imagerouter.io/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl command examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and an ImageRouter API key; examples may reference local image or mask file paths for image-to-image and inpainting workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
