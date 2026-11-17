## Description:

Helps an agent create AI travel photos by submitting a user-approved portrait and scenic-place name to Migu's creative-photo service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llforest](https://clawhub.ai/user/llforest)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can ask an agent to combine their portrait with a named travel destination, then receive links to the generated photos after authorizing the upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service receives personal portraits, gender/category, and the scenic-place name.

Mitigation: Explain the external transfer and obtain the user's approval before each upload and generation request.

Risk: A Migu JWT stored in the skill directory could be exposed to other users of the device.

Mitigation: Keep the JWT file private and do not share the skill directory with other users.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/llforest/skills/migu-ai-creative-photo)
- [Migu creative-photo service](https://gulangyu.migudm.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Text or Markdown with links to generated photos]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns photo links only when the service reports completed results; generation can require polling.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; bundled package.json states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
