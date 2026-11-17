## Description:

Tencent Cloud Hunyuan Image Generation 3.0 generates images from text prompts or reference-image guided prompts with controls for resolution, seed, and prompt rewriting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neck-cn](https://clawhub.ai/user/neck-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to submit Tencent Cloud Hunyuan text-to-image or image-guided generation jobs, poll for completion, and retrieve generated image URLs. It is suited for agent workflows that need scripted image generation through Tencent Cloud credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference image URLs are sent to Tencent Cloud during image generation.

Mitigation: Use the skill only with data approved for Tencent Cloud processing and avoid sending confidential prompts or sensitive image URLs.

Risk: The skill can install the Tencent Cloud Python SDK at runtime without a pinned dependency version.

Mitigation: Run it in an isolated environment with the SDK preinstalled and pinned before enabling normal use.

Risk: The skill handles Tencent Cloud credentials from environment variables.

Mitigation: Scope Tencent Cloud credentials to the minimum image-generation permissions needed and rotate or revoke them if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neck-cn/skills/hy-image-generation)
- [Tencent Cloud SubmitTextToImageJob API](https://cloud.tencent.com/document/product/1668/124632)
- [Tencent Cloud QueryTextToImageJob API](https://cloud.tencent.com/document/product/1668/124633)
- [Submit text-to-image API reference](references/submit_text_to_image_api.md)
- [Query text-to-image API reference](references/query_text_to_image_api.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [JSON responses containing job IDs, status, generated image URLs, result details, revised prompts, and errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image URLs are temporary and the skill reports that they expire after 1 hour.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
