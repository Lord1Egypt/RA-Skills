## Description: <br>
Converts PDFs to Markdown, JSON, and HTML with OCR, layout analysis, table extraction, and bounding-box data for RAG, document parsing, and batch PDF workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adelpro](https://clawhub.ai/user/adelpro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide PDF-to-Markdown, JSON, and HTML conversion for RAG pipelines, research-paper parsing, scanned document OCR, table extraction, accessibility, and content migration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installation guidance includes an unpinned remote script piped directly into bash. <br>
Mitigation: Prefer installing opendataloader-pdf with pip in a virtual environment or container; if using the remote installer, fetch and inspect it first and verify the source. <br>
Risk: Converted outputs may expose sensitive PDF contents, OCR text, document metadata, and page coordinates. <br>
Mitigation: Treat generated Markdown, JSON, and HTML as sensitive when processing private PDFs and store or share them only under the same controls as the source documents. <br>


## Reference(s): <br>
- [ODL PDF to Markdown on ClawHub](https://clawhub.ai/adelpro/odl-pdf-to-markdown) <br>
- [OpenDataLoader PDF](https://github.com/opendataloader-project/opendataloader-pdf) <br>
- [PDF/UA](https://pdfa.org) <br>
- [veraPDF](https://verapdf.org) <br>
- [ClawHub](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides workflows that produce Markdown, JSON, and HTML files from PDFs, including optional OCR and bounding-box JSON for source citations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
