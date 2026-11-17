## Description:

Convert markdown files to clean, formatted PDFs using reportlab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[araa47](https://clawhub.ai/user/araa47)

### License/Terms of Use:


## Use Case:

Developers and content authors use this skill to convert Markdown documents into formatted PDF files from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter installs an unpinned reportlab dependency at runtime.

Mitigation: Pin or lock the reportlab dependency before use in sensitive or controlled environments.

Risk: The script reads Markdown input and referenced local image paths and writes a PDF file.

Mitigation: Run it with filesystem access limited to the intended input and output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/araa47/skills/md-2-pdf)

## Skill Output:

**Output Type(s):** [shell commands, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with command-line examples; the script produces PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and installs reportlab at runtime unless dependency resolution is pinned externally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
