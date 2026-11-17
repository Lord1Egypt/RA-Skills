## Description:

Convert a finished raster image, especially a generated poster or visual resume, into an image-based PDF with an additional selectable, copyable, searchable text layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjsxply](https://clawhub.ai/user/zjsxply)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and document automation users use this skill to turn final raster designs into PDFs that preserve the exact image while adding selectable, copyable, and searchable text. It is especially useful when recreating the visual layout in presentation, web, or LaTeX formats would be fragile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive document text can be exposed in terminal logs when using text-checking output.

Mitigation: Avoid using --check-text on sensitive documents in logged terminals.

Risk: The invisible text layer can contain incorrect or poorly aligned copyable text if OCR correction or layout boxes are wrong.

Mitigation: Review the debug PDF and copied text before sharing the final PDF.

Risk: Non-Latin text may not extract correctly if the default PDF font lacks required glyphs.

Mitigation: Provide an appropriate Unicode font file for CJK or other non-Latin text.

## Reference(s):

- [Layout JSON](references/layout-json.md)
- [OCR and Source-Text Alignment](references/ocr-alignment.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON layout configuration; generated workflow artifacts are PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a final image-based PDF with an invisible text layer and an optional visible debug PDF for inspection.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
