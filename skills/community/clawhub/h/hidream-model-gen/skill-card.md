## Description:

Generate images and videos using Vivago AI (智小象) platform, including text-to-image, image-to-image, image-to-video, and keyframe-to-video generation through the Vivago AI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhy2015](https://clawhub.ai/user/zhy2015)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate or transform images and videos with Vivago AI from prompts, source images, keyframes, or predefined video templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, images, and generation metadata are sent to Vivago using the user's account token.

Mitigation: Use the skill only with content approved for Vivago processing and avoid submitting sensitive or restricted data.

Risk: Vivago token handling is under-scoped in the security evidence.

Mitigation: Provide the token through HIDREAM_AUTHORIZATION, avoid exposing it in command history or logs, and rotate the token if it may have been disclosed.

Risk: Template data may include adult audio or video behavior that is not clearly disclosed.

Mitigation: Review and remove adult templates before use in general-audience or policy-restricted environments.

Risk: Untrusted custom ports configuration can change API endpoints or generation behavior.

Mitigation: Use only trusted configuration files and review endpoint changes before running generation commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhy2015/skills/hidream-model-gen)
- [Vivago AI](https://vivago.ai/)
- [Vivago Token Endpoint](https://vivago.ai/prod-api/user/token)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with Python and shell examples; CLI tools write JSON result files and media URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image and video assets are created through Vivago API calls and may be written to local output paths.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
