## Description:

Generates QR code images for text, URLs, and WiFi configuration content, with configurable size, color, and save path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayxu-d](https://clawhub.ai/user/jayxu-d)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn provided text, URLs, phone numbers, or WiFi connection details into QR code image files saved at a requested path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run unpinned pip installs automatically when its Python module is loaded, changing the agent's Python environment.

Mitigation: Remove automatic installation from module import, declare pinned dependencies in installation metadata, and install them through an explicit reviewed setup step.

Risk: The skill writes image files to a user-supplied path or to the Desktop by default.

Mitigation: Ask the user to confirm the destination path before writing and prefer a constrained output directory with expected write permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayxu-d/skills/my-generate-qr-code)

## Skill Output:

**Output Type(s):** [text, files, code, guidance]

**Output Format:** [Text status message and generated PNG image file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a QR code image to the requested path, defaulting to the user's Desktop when no save path is provided.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
