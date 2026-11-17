## Description:

Uses a Nano Banana API key, a prompt, and optional input images to test text-to-image and image-to-image generation and save the resulting images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flywhale-666](https://clawhub.ai/user/flywhale-666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run real Nano Banana text-to-image or image-to-image generation checks from user-supplied prompts, optional source images, and an API key. It returns command-driven test results and generated image paths for validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store the Nano Banana API key in a local plaintext credentials file.

Mitigation: Use only trusted machines, avoid sharing the account, and delete or rotate the saved key when the machine or account is shared.

Risk: A custom API base URL option could send the API key and images outside the intended service.

Mitigation: Use the default trusted service endpoint and do not pass a custom --base-url unless the publisher and endpoint are explicitly trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flywhale-666/skills/nano-banana-image-t8-windows)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands, status text, and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated PNG files under the user's WhaleClaw workspace and may save a local Nano Banana API key file.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
