## Description:

jpocr extracts Japanese text from images and scanned pages locally using NDLOCR-Lite, with support for printed, vertical, English, and experimental handwritten text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realwaynesun](https://clawhub.ai/user/realwaynesun)

### License/Terms of Use:


## Use Case:

Developers and agents use jpocr to run local OCR on Japanese document images or directories and return text, JSON bounding boxes, or visualization outputs without a GPU or API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes local image files and writes OCR outputs under its output directory.

Mitigation: Use trusted input paths and review generated text, JSON, and visualization files before relying on them.

Risk: The wrapper has shell-hardening issues around paths with spaces or option-like segments.

Mitigation: Prefer simple paths without spaces or leading hyphen segments until the wrapper is hardened.

Risk: The wrapper expects local OCR implementation files and dependencies that should be present before use.

Mitigation: Verify the Python environment, OCR implementation, and required model dependencies before deploying or relying on the skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands]

**Output Format:** [Plain text, JSON with bounding boxes, or generated visualization image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes a single image path or directory path and writes OCR output under the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
