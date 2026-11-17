## Description:

Convert PowerPoint PPTX files to high-quality JPG or PNG slide images with configurable DPI while preserving original slide proportions and orientation on Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leodai12123](https://clawhub.ai/user/leodai12123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation users, and content teams use this skill to convert PowerPoint presentations into image assets for publishing, review, archival, or downstream processing. It is intended for Windows environments with Microsoft PowerPoint and pywin32 installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter automates Microsoft PowerPoint on Windows and may open Office documents supplied by users.

Mitigation: Convert only trusted presentations or run the conversion in a low-privilege, disposable Windows environment.

Risk: The skill depends on pywin32 and a local Microsoft PowerPoint installation.

Mitigation: Use a virtual environment, pin pywin32 before use, and verify PowerPoint 2010 or later is installed before relying on the conversion workflow.

Risk: High-DPI exports can create large per-slide image files.

Mitigation: Choose lower DPI for previews and confirm output storage capacity before batch conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leodai12123/skills/pptx-to-image)

## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [JPG or PNG image files with plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configurable input path, output folder, DPI from 72 to 600, image format, JPG quality, and verbose progress reporting.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
