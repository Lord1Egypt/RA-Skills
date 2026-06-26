## Description: <br>
Provides a PDF processing toolkit for extracting text and tables, creating, merging, splitting, rotating, watermarking, password-protecting, OCRing, and filling PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document automation users use this skill to inspect, transform, generate, and fill PDFs, including scanned or non-fillable forms, through guided Python and command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDFs and generated intermediates can contain sensitive personal, medical, financial, or legal information. <br>
Mitigation: Process only documents you are comfortable sharing with the agent, keep generated PNG, JSON, text, and filled PDF files protected, and delete intermediates when finished. <br>
Risk: Non-fillable form workflows can place text or checkbox marks incorrectly if bounding boxes are inaccurate. <br>
Mitigation: Use the validation-image and bounding-box checks described by the artifact, then visually inspect the filled PDF before relying on it. <br>
Risk: PDF transformations and form filling can change document appearance or field behavior across PDF viewers. <br>
Mitigation: Open the generated PDF in the intended viewer and confirm text, tables, annotations, fields, and page layout before submission or distribution. <br>
Risk: OCR and extraction workflows may be incomplete or inaccurate for scanned, complex, or damaged PDFs. <br>
Mitigation: Validate extracted text and tables against the original document and use OCR or repair steps only as aids, not as authoritative review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wu-uk/jpg-ocr-stat-pdf) <br>
- [PDF Processing Guide](artifact/SKILL.md) <br>
- [PDF Form Filling Guide](artifact/forms.md) <br>
- [PDF Processing Advanced Reference](artifact/reference.md) <br>
- [Adobe PDF 32000:2008 specification](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448) <br>
- [Exploring fillable forms with pdfrw](https://westhealth.github.io/exploring-fillable-forms-with-pdfrw.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, JavaScript, shell command snippets, and JSON field files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workflows may create or modify local PDF, PNG, text, table, and JSON files when the provided scripts are run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
