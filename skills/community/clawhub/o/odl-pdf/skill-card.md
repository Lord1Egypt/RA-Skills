## Description: <br>
Convert any PDF to Markdown, JSON, and HTML using OpenDataLoader, including digital PDFs, scanned PDFs with OCR, and complex layouts with table extraction and reading-order detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adelpro](https://clawhub.ai/user/adelpro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing teams use this skill to convert PDFs into readable markdown, structured JSON, or HTML for RAG pipelines, search, accessibility, data extraction, and content migration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The auto-install path runs an unpinned remote shell script. <br>
Mitigation: Review and download the installer before execution, or prefer pinned package-manager installation in a virtual environment or container. <br>
Risk: PDF conversion can expose document contents in generated output files. <br>
Mitigation: Process only PDFs the user is authorized to expose, and store generated Markdown, JSON, and HTML outputs in appropriately protected locations. <br>
Risk: Java, Python, OCR, and local executable setup can affect the host environment. <br>
Mitigation: Install dependencies in an isolated virtual environment or container and verify Java paths before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adelpro/odl-pdf) <br>
- [ClawHub homepage](https://clawhub.com) <br>
- [OpenDataLoader PDF](https://github.com/opendataloader-project/opendataloader-pdf) <br>
- [PDF/UA](https://pdfa.org) <br>
- [veraPDF](https://verapdf.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, Python snippets, and examples of generated Markdown, JSON, and HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files may include extracted PDF text, layout metadata, bounding boxes, font information, page numbers, OCR output, tables, and HTML layout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
