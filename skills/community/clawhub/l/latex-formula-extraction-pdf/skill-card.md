## Description: <br>
Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to process PDF documents, extract text and tables, generate or transform PDFs, and fill either fillable or image-based PDF forms with validation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decrypted PDFs, generated JSON, PNG, and PDF outputs may contain sensitive document data. <br>
Mitigation: Work on copies in a controlled folder, delete intermediates when finished, and only decrypt PDFs when authorized. <br>
Risk: Incorrect form-field values or bounding boxes can produce inaccurate completed PDFs. <br>
Mitigation: Use the included field validation and bounding-box checks, inspect validation images, and review the final PDF before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wu-uk/latex-formula-extraction-pdf) <br>
- [PDF form workflow](artifact/forms.md) <br>
- [PDF processing advanced reference](artifact/reference.md) <br>
- [Adobe PDF 32000-1:2008 standard](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, JSON, PDF files, PNG images] <br>
**Output Format:** [Markdown guidance with inline code blocks; helper scripts emit JSON, PNG, and PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local PDF processing; generated intermediates can include extracted form fields, validation images, and modified PDFs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
