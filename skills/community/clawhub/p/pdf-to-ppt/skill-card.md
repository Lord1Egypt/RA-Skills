## Description:

Convert PDF files to PowerPoint presentations via intermediate image rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvtop](https://clawhub.ai/user/jvtop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document workflow users use this skill to convert visual PDFs, scanned presentation material, design drawings, and similar documents into PPTX slide decks while preserving each PDF page as a slide image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing dependencies into the system Python environment can affect other Python tools.

Mitigation: Use a virtual environment before installing PyMuPDF and python-pptx.

Risk: Default output and image paths write next to the source PDF and can replace existing generated files.

Mitigation: Use explicit --output and --img-dir paths for each conversion.

Risk: The generated slides contain rendered page images rather than selectable PowerPoint text, and images are stretched to fill slides.

Mitigation: Review generated slides before use and choose a text-preserving or aspect-ratio-preserving workflow when those properties matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jvtop/skills/pdf-to-ppt)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and generated PPTX/image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a PPTX file and optional intermediate PNG or JPG page images on the local filesystem.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
