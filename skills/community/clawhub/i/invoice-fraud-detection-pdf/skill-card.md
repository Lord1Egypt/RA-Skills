## Description: <br>
Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and agents use this skill to process user-provided PDFs, extract text and tables, create or modify documents, and fill PDF forms with validation steps for fillable and non-fillable forms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF contents, extracted text, form values, validation images, and JSON metadata may contain sensitive information. <br>
Mitigation: Use only PDFs the user explicitly provides, work on copies of important files, handle generated artifacts as sensitive, and delete temporary outputs when finished. <br>
Risk: PDF decryption or protection removal can be unauthorized or inappropriate. <br>
Mitigation: Only decrypt or remove protection from PDFs that the user is authorized to handle. <br>
Risk: Optional PDF tooling and OCR dependencies may execute local code or process untrusted files. <br>
Mitigation: Install optional dependencies from trusted sources and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/invoice-fraud-detection-pdf) <br>
- [PDF Processing Guide](artifact/SKILL.md) <br>
- [PDF Form Filling Guide](artifact/forms.md) <br>
- [PDF Processing Advanced Reference](artifact/reference.md) <br>
- [Adobe PDF 32000:2008 reference](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, JavaScript, shell command, JSON, and PDF file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local PDFs, page images, validation images, extracted text, tables, and JSON metadata from user-provided documents.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
