## Description:

Generates and edits images through the Guishu Images API, including reference-image edits, masked edits, batch generation, and recovery of existing image downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quqi1599](https://clawhub.ai/user/quqi1599)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents who explicitly choose Guishu's image service can use this skill to generate images, edit reference images or masked regions, submit batches, and recover saved results. It is not intended for image understanding or for replacing a provider selected by the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send prompts and selected images to Guishu and may incur charges; provider retention and live billing behavior were not verified.

Mitigation: Use the service only if its charges and handling of submitted material are acceptable, use a dedicated Guishu key, and send only task-specific images.

Risk: An interrupted generation request may already have been accepted, leaving its result and charge status uncertain.

Mitigation: Check service usage before retrying and use recovery on saved responses; do not automatically resubmit an uncertain request.

Risk: Recovery files can contain image data or temporary signed download URLs.

Mitigation: Keep recovery files in a private location and do not upload them to public repositories.

## Reference(s):

- [ClawHub release](https://clawhub.ai/quqi1599/guishu-gpt-image-2)
- [Guishu GPT Image 2 tutorial](https://llm-token.cn/tutorials/gpt-image-2)
- [Guishu Skills support](https://llm-token.cn/tutorials/skills-support)

## Skill Output:

**Output Type(s):** [Images, JSON, Shell commands, Guidance]

**Output Format:** [PNG, JPEG, or WebP image files, with an optional JSON task summary and Markdown usage guidance]

**Output Parameters:** [1D; configurable image size, quality, format, and count, with optional batches of prompts]

**Other Properties Related to Output:** [Local image results and recovery state; generated results depend on the selected model and service availability.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
