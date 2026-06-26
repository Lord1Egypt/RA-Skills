## Description: <br>
Converts PDFs to Markdown, JSON, and HTML using OpenDataLoader, including digital PDFs, scanned PDFs with OCR, and complex layouts with table extraction and reading-order detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adelpro](https://clawhub.ai/user/adelpro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing teams use this skill when a user provides a PDF and needs readable text, structured data, or searchable content for RAG pipelines, accessibility, content migration, or data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional remote install command may execute code from a remote script. <br>
Mitigation: Prefer the pip install path, or inspect the remote install script before running it. <br>
Risk: Converted Markdown, JSON, and HTML files may contain confidential content from source PDFs. <br>
Mitigation: Process confidential PDFs only in trusted directories, review generated outputs before sharing, and delete extracted files when no longer needed. <br>
Risk: OCR, table extraction, and reading-order detection can produce imperfect results on complex or scanned PDFs. <br>
Mitigation: Review important generated content against the original PDF before relying on it in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adelpro/odl-pdf-parser) <br>
- [ClawHub metadata homepage](https://clawhub.com) <br>
- [OpenDataLoader PDF](https://github.com/opendataloader-project/opendataloader-pdf) <br>
- [PDF/UA](https://pdfa.org) <br>
- [veraPDF](https://verapdf.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides conversion of PDF files into Markdown, JSON, and HTML outputs; Java 11+ and Python 3.10+ are prerequisites.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
