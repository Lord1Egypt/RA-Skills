## Description:

Enhances photos with a Canon IXUS 130 CCD-style effect and an optional custom bottom watermark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x0cd](https://clawhub.ai/user/x0cd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to apply a CCD-style photo enhancement and optionally add a text watermark to uploaded images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large, malformed, or untrusted image inputs may create reliability or resource-use issues during image processing.

Mitigation: Use the skill with trusted or size-limited images and add strict file size, dimension, pixel-count, format validation, and error handling before broader deployment.

Risk: The image-processing dependency is not pinned by a lockfile in the artifact.

Mitigation: Pin and review dependency versions before installing or deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x0cd/skills/pixcakeai)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Image, Files]

**Output Format:** [Base64-encoded JPEG image]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JPEG quality 95%, progressive encoding, with optional bottom text watermark]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
