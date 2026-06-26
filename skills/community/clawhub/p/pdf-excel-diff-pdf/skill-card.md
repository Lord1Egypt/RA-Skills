## Description: <br>
A comprehensive PDF manipulation toolkit for extracting text and tables, creating and modifying PDFs, merging and splitting documents, and handling fillable and non-fillable forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
Proprietary. LICENSE.txt has complete terms <br>


## Use Case: <br>
Developers and agents use this skill to read, generate, transform, merge, split, and fill PDF documents, including extracting structured tables and creating supporting files for form workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF workflows may create intermediate images, JSON field maps, or filled PDFs that contain sensitive document data. <br>
Mitigation: Use only PDFs you are authorized to access, choose non-conflicting output paths, review generated files before sharing, and delete sensitive intermediate files when work is complete. <br>
Risk: Form-field extraction and bounding-box workflows can produce incorrect placements on complex or scanned PDFs. <br>
Mitigation: Validate field IDs, bounding boxes, and rendered output before relying on completed forms or derived documents. <br>


## Reference(s): <br>
- [ClawHub release](https://clawhub.ai/lnj22/pdf-excel-diff-pdf) <br>
- [PDF form workflow guide](artifact/forms.md) <br>
- [Advanced PDF processing reference](artifact/reference.md) <br>
- [Adobe PDF 32000-1:2008 reference](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local PDF, image, JSON, text, and spreadsheet files when an agent follows the workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
