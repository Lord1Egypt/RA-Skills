## Description: <br>
All-in-one PDF processing tool for merging, splitting, extracting, converting, OCR, table recognition, PDF-to-image conversion, and PDF form workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonicrang](https://clawhub.ai/user/sonicrang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to select and run local PDF workflows for extracting text and tables, converting pages to images, OCR, merging and splitting PDFs, and filling PDF forms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local PDF processing can create text, JSON, image, spreadsheet, and modified-PDF intermediates that expose sensitive document contents. <br>
Mitigation: Use a controlled workspace, process only PDFs you own or are authorized to process, and delete sensitive intermediate files when finished. <br>
Risk: Password-protected PDF examples include command-line password usage, which can expose secrets through shell history or process listings. <br>
Mitigation: Avoid placing real passwords directly in commands; prefer secure input methods or temporary test credentials. <br>
Risk: Repair, decrypt, merge, split, and form-filling operations can alter PDFs or create incorrect outputs. <br>
Mitigation: Keep backups of source PDFs and review generated files, validation images, and form field values before relying on the result. <br>


## Reference(s): <br>
- [PDF All-in-One ClawHub Page](https://clawhub.ai/sonicrang/pdf-all-in-one) <br>
- [Publisher Profile](https://clawhub.ai/user/sonicrang) <br>
- [OpenClaw Fork Metadata](https://github.com/anthropics/skills) <br>
- [Forms Guide](artifact/forms.md) <br>
- [PDF Processing Advanced Reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python, JavaScript, and shell command snippets; bundled scripts can produce PDF, PNG, JSON, text, and spreadsheet files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local filesystem outputs may contain extracted PDF content, form data, rendered page images, or modified PDFs.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.release.version and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
