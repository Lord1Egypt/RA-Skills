## Description:

Image Edit — Pro Pack on RunComfy helps an agent route image-edit requests to RunComfy edit models for background swaps, object changes, text rewrites, mask-based edits, multi-reference composition, and batch edits up to 20 inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn an existing image plus an edit instruction into RunComfy CLI calls for the appropriate image-edit endpoint. It is suited for product imagery, creative production, localization, retouching, and mask-based image replacement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the external RunComfy CLI and a RunComfy account.

Mitigation: Install a reviewed pinned CLI version, avoid sudo, and use a least-privileged RunComfy token.

Risk: Image URLs, masks, prompts, and generated outputs are sent through RunComfy.

Mitigation: Use the skill only for images appropriate for that external processing path and avoid sensitive image data unless the account and workflow are approved.

Risk: Source images and masks may come from third-party URLs.

Mitigation: Treat external image and mask URLs as untrusted inputs and review outputs before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/image-edit-runcomfy)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=image-edit-runcomfy)
- [RunComfy image edit models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=image-edit-runcomfy)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces RunComfy CLI invocations and routing guidance; generated image files are downloaded by the external RunComfy CLI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
