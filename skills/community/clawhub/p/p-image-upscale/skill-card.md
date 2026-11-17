## Description:

Guides agents in upscaling or sharpening an existing image for print, large crops, or higher-quality delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pruna-ai](https://clawhub.ai/user/pruna-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to prepare existing images for larger prints or crops through Pruna's hosted upscaling service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Related-skill installation commands are not pinned to specific versions.

Mitigation: Verify the PrunaAI source and pin trusted versions before installation.

Risk: The workflow sends source images and API credentials to Pruna's hosted service.

Mitigation: Use only images and credentials approved for submission to that service.

Risk: Disabling the safety checker can affect policy compliance and outputs.

Mitigation: Keep the safety checker enabled unless the implications have been reviewed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/pruna-ai/skills/p-image-upscale)
- [Pruna p-image-upscale model documentation](https://docs.api.pruna.ai/guides/models/p-image-upscale)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers image upload, target resolution, enhancement options, and output format.]

## Skill Version(s):

1.0.15 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
