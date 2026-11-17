## Description:

Converts text-layer academic PDFs into clean Markdown, with layout-aware reading order, figure extraction, and batch processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ogzhnbygl](https://clawhub.ai/user/ogzhnbygl)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and analysts use this skill to convert local digital academic PDFs, individually or in batches, into readable Markdown for reading, quoting, and analysis. It preserves academic reading order and can extract figures alongside the text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF parsing depends on PyMuPDF, so an outdated dependency may lack security fixes.

Mitigation: Use a maintained, patched PyMuPDF release and record its exact version.

Risk: Batch conversion can overwrite files when output names collide.

Mitigation: Choose a separate output directory and check for naming collisions before batch conversion.

Risk: Bibliographies are removed by default, which may omit needed source references.

Mitigation: Select --keep-references when the bibliography is needed, then review the converted output.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/ogzhnbygl/pdfparse)
- [Imported source commit](https://github.com/ogzhnbygl/pdfparse/commit/010008df0adc8e66931ea1c2a682b99ec90eec76)
- [ClawHub release page](https://clawhub.ai/ogzhnbygl/skills/pdfparse)
- [PyMuPDF documentation](https://pymupdf.readthedocs.io/)

## Skill Output:

**Output Type(s):** [Files, Markdown, JSON]

**Output Format:** [Markdown text files with optional extracted figure images; optional JSON conversion summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one or more local PDFs; output can include page markers and retained references when requested. Scanned PDFs without a text layer are reported as empty rather than OCR-processed.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata; source CHANGELOG identifies 2.0.0, released 2026-10-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
