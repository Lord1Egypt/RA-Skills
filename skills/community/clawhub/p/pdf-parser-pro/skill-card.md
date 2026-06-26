## Description: <br>
Convert any PDF to Markdown, JSON, and HTML using OpenDataLoader, including digital PDFs, scanned PDFs with OCR, and complex layouts with table extraction and reading-order detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adelpro](https://clawhub.ai/user/adelpro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing teams use this skill to convert PDFs into readable Markdown, structured JSON, or HTML for search, RAG pipelines, data extraction, accessibility, and content migration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installation instructions include a mutable remote shell installer. <br>
Mitigation: Prefer manual installation with pip and OS package-manager Java/OCR dependencies, or inspect and verify the installer before running it in an acceptable environment. <br>
Risk: PDF parsing and OCR may produce incomplete or incorrect text, table structure, or reading order for complex documents. <br>
Mitigation: Review converted output before using it in search, RAG, data extraction, accessibility, or migration workflows. <br>


## Reference(s): <br>
- [PDF to Markdown ClawHub listing](https://clawhub.ai/adelpro/pdf-parser-pro) <br>
- [OpenDataLoader PDF](https://github.com/opendataloader-project/opendataloader-pdf) <br>
- [PDF/UA](https://pdfa.org) <br>
- [veraPDF](https://verapdf.org) <br>
- [ClawHub homepage](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI commands, Python code examples, and structured JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The described conversion outputs can include Markdown, JSON with layout metadata, and HTML.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
