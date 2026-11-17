## Description:

Converts a Mac PowerPoint file into per-slide PNG screenshots and tiled thumbnail sheets with configurable DPI and layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxm8023](https://clawhub.ai/user/zhaoxm8023)

### License/Terms of Use:


## Use Case:

Developers and Mac users use this skill to configure and run a local workflow that converts PPT or PPTX presentations into PNG slide images and thumbnail contact sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users for WeChat app credentials even though the included code does not use or justify them.

Mitigation: Do not provide WeChat app secrets unless the publisher documents why they are needed and how they are protected.

Risk: The workflow executes local LibreOffice and Ghostscript binaries against user-selected presentation and PDF content.

Mitigation: Use only trusted local binaries and input files, and verify the configured executable paths before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxm8023/skills/ppt2png)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with configuration values and shell commands; the runtime produces local PNG slide images and thumbnail files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-selected PowerPoint input, output folder, DPI, thumbnail rows and columns, LibreOffice path, and Ghostscript path.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
