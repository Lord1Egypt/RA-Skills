## Description:

Add accurate, publication-ready scale bars to microscopy images given pixel-to-unit calibration data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and microscopy researchers use this skill to add calibrated scale bars to TIFF, PNG, JPG, or BMP microscopy images for publication figures and batch image preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the script can read from or write to absolute paths outside the workspace despite claiming those paths are blocked.

Mitigation: Use trusted image paths and explicit output locations only; fix path validation to reject absolute paths, resolve symlinks, and avoid overwriting files unless explicitly requested before relying on workspace isolation.

Risk: Incorrect or missing calibration data can produce misleading scale bars.

Mitigation: Require explicit pixels-per-unit data when TIFF calibration metadata is unavailable, and do not fabricate scale values or calibration assumptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/microscopy-scale-bar-adder)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown response with CLI commands, fallback reports when blocked, and generated annotated image file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit image paths and calibration data; outputs depend on Pillow image processing and user-supplied or TIFF-derived pixels-per-unit values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
