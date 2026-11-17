## Description:

Generates images from text prompts using the included Ark/VolcEngine image generation script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangsiyuan123123](https://clawhub.ai/user/zhangsiyuan123123)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and external users can use this skill to generate images from clear text prompts and save the generated outputs locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generation requests are sent to an Ark/VolcEngine image-generation service.

Mitigation: Avoid sending sensitive prompts unless the service and account are approved for that data.

Risk: The script uses image-generation credentials from environment variables.

Mitigation: Use scoped API keys and rotate or revoke credentials according to local policy.

Risk: Generated images are downloaded to the current directory or IMAGE_DOWNLOAD_DIR.

Mitigation: Set IMAGE_DOWNLOAD_DIR to a private, trusted directory rather than a shared or attacker-writable path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhangsiyuan123123/skills/image-generate)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Configuration]

**Output Format:** [Local image files with terminal status or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Ark/VolcEngine credentials; model and download directory can be set with environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
