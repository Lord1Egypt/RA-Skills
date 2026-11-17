## Description:

PDF Tools helps agents view, extract, edit, merge, split, rotate, and inspect PDF documents using bundled Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cmpdchtr](https://clawhub.ai/user/cmpdchtr)

### License/Terms of Use:

MIT License

## Use Case:

Developers and external users use this skill to automate common PDF document tasks such as extracting content, inspecting metadata, reorganizing pages, combining files, rotating pages, and adding simple text overlays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF operations can write new files or overwrite an existing file if the user selects the same output path.

Mitigation: Use explicit output paths, keep backups for important PDFs, and avoid reusing the original file path unless overwriting is intended.

Risk: Unpinned Python dependencies may change behavior across environments.

Mitigation: Install the skill in a virtual environment and pin pdfplumber, PyPDF2, and reportlab versions.

Risk: PDF text replacement is limited and may fail or produce unexpected document changes because PDF text encoding and layout are complex.

Mitigation: Prefer text overlays for simple additions, and use an extract, edit, and regenerate workflow for complex edits.

Risk: Text extraction does not include OCR and works best on text-based PDFs.

Mitigation: Use a separate OCR workflow for scanned PDFs before relying on extracted text.

## Reference(s):

- [PDF Libraries Reference](references/libraries.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated local PDF or text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some scripts can write PDF, text, or JSON outputs to user-specified local paths.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
