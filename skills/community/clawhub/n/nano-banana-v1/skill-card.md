## Description:

Nano Banana Pro Cn helps agents generate and edit images from natural-language prompts through APIYi's NanoBananaPro image-generation service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to generate new images or edit selected input images from user prompts. It supports command-line image generation with selectable aspect ratios, 1K/2K/4K resolution options, and Node.js or Python execution paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input images are sent to APIYi and its downstream provider for external processing.

Mitigation: Use the skill only when that external processing is acceptable, and avoid private, confidential, medical, financial, or regulated images or text unless approved.

Risk: Passing the API key on the command line may expose it through shell history or process metadata.

Mitigation: Prefer the APIYI_API_KEY environment variable or a managed secret for the API key.

Risk: External image generation can take time or fail because of network, provider, or timeout conditions.

Mitigation: Expect long-running requests, handle failures, and verify the generated output file before using it downstream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/nano-banana-v1)
- [APIYi](https://apiyi.com/)
- [APIYi API console](https://api.apiyi.com)
- [Usage scenarios](artifact/references/scene.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with command-line invocations; generated PNG image files from the helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an APIYi API key; optional inputs include prompt text, output filename, aspect ratio, resolution, and up to 14 input images for editing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
