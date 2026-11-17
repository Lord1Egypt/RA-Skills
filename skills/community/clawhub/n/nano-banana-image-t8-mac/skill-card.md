## Description:

Runs Nano Banana image generation tests with a user-provided API key and prompt, supporting text-to-image and image-to-image workflows with optional size or aspect ratio settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flywhale-666](https://clawhub.ai/user/flywhale-666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and image-generation users use this skill to run Nano Banana text-to-image and image-to-image requests from an agent session, passing prompts, optional input images, and optional size or aspect ratio settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses a Nano Banana API key on disk.

Mitigation: Use a limited, revocable API key, avoid shared machines, and rotate or delete the saved key when access is no longer needed.

Risk: API key handling could expose credentials to unintended URLs if the API host is changed.

Mitigation: Keep the base URL fixed to the documented service host and do not override it during normal use.

Risk: The security verdict is suspicious because credential handling is not yet low risk.

Mitigation: Review the security guidance before deployment and require publisher-side host validation, unauthenticated image downloads, and an explicit key deletion or non-persistent mode before treating the skill as low risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flywhale-666/skills/nano-banana-image-t8-mac)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown or plain text with shell commands, API status details, and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated PNG files are saved under ~/.whaleclaw/workspace/nano_banana_test by default.]

## Skill Version(s):

0.1.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
