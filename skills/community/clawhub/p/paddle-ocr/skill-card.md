## Description: <br>
Converts legal PDFs and scanned documents into editable Markdown with PaddleOCR-based structure extraction, table recognition, formula recognition, layout analysis, and traceable archive outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cat-xierluo](https://clawhub.ai/user/cat-xierluo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Legal professionals, developers, and document-processing teams use this skill to convert local PDFs or common image files into Markdown for legal review, evidence extraction, knowledge-base ingestion, and downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive documents may be sent to a configured OCR API endpoint. <br>
Mitigation: Use only a trusted local or controlled endpoint for privileged legal, medical, or confidential records, and use page selection to minimize uploaded content. <br>
Risk: The workflow can save local copies of source files, extracted text, JSON results, and images in an archive. <br>
Mitigation: Use no-archive mode when retention is not needed, and delete generated archives and image folders after review. <br>
Risk: Network behavior depends on the configured OCR endpoint and token. <br>
Mitigation: Review the endpoint configuration before execution and avoid running the skill against endpoints that are not approved for the document sensitivity. <br>


## Reference(s): <br>
- [Output structure reference](references/output_schema.md) <br>
- [PaddleOCR official site](https://www.paddleocr.com) <br>
- [ClawHub skill page](https://clawhub.ai/cat-xierluo/paddle-ocr) <br>
- [Metadata homepage](https://github.com/cat-xierluo/legal-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [Markdown files with JSON archive artifacts and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write an archive containing the source file copy, result Markdown, result JSON, batch JSON files, extracted images, and metadata; supports page selection and a no-archive mode.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata, skill frontmatter, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
