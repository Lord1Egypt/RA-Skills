## Description:

Extracts and saves QR codes from each page of a PDF by converting pages to images and detecting QR regions with padding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mywebliu](https://clawhub.ai/user/mywebliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to extract QR code images from customer-provided PDFs in batch workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation guidance uses an overbroad Python package command that can modify the system Python environment.

Mitigation: Install dependencies in an isolated virtual environment, remove the separate fitz package, pin dependencies, and avoid --break-system-packages.

Risk: Generated page images and QR crops may contain sensitive information from the source PDF.

Mitigation: Treat outputs as sensitive and delete the output directory when processing is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mywebliu/skills/pdf-qr-extractor)
- [Publisher profile](https://clawhub.ai/user/mywebliu)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates QR crop PNG files in the output directory and stores rendered PDF page images in a pages subdirectory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
