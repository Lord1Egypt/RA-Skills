## Description:

Generate QR codes from text, URLs, or images, including local images that are automatically compressed when possible.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nbf819-web](https://clawhub.ai/user/nbf819-web)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to create QR code images from text, URLs, or explicitly provided local image files for sharing or scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image mode can read and encode arbitrary small local files when given a path.

Mitigation: Use only trusted, explicit image paths; avoid secrets or private configuration files; restrict allowed paths and validate image contents before deployment.

Risk: Generated QR codes may embed sensitive or unintended local data.

Mitigation: Review input content and generated QR output before sharing, and prefer URLs for image sharing when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nbf819-web/skills/pr-generator)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [JSON-compatible object containing an image path, error, or message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates PNG QR code files in the system temporary directory.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
