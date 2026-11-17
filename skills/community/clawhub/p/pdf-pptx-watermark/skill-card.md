## Description:

Converts PPT/PPTX or PDF files into watermarked PDFs with configurable text, opacity, rotation, color, and diagonal, grid, or center layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avocadoleaf-highfive](https://clawhub.ai/user/avocadoleaf-highfive)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and document owners use this skill to convert presentations to PDF or apply configurable watermarks to PDFs before internal sharing, batch distribution, or client delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document conversion and PDF rewriting run locally on user-supplied files.

Mitigation: Run the tool in a virtual environment without administrator/root privileges and keep input and output paths separate.

Risk: The resulting watermark may not match expectations or may fail to cover all relevant document content.

Mitigation: Review the generated PDF before distribution or relying on the watermark.

Risk: Phone or live-tuning claims may overstate the artifact's UI behavior.

Mitigation: Treat the included UI as static preview and JSON configuration support unless the publisher documents a real QR/mobile synchronization workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/avocadoleaf-highfive/skills/pdf-pptx-watermark)
- [Project homepage](https://github.com/AvocadoLeaf-Highfive/pdf-pptx-watermark)
- [Mobile parameter tuning](https://github.com/AvocadoLeaf-Highfive/pdf-pptx-watermark#mobile-parameter-tuning)
- [Watermark effects](https://github.com/AvocadoLeaf-Highfive/pdf-pptx-watermark#watermark-effects)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration; generated output is a PDF file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and a LibreOffice-compatible soffice binary for PPT/PPTX conversion.]

## Skill Version(s):

1.5.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
