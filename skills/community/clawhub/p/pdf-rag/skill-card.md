## Description: <br>
Convert any PDF to Markdown, JSON, and HTML using OpenDataLoader, including digital PDFs, scanned PDFs with OCR, and complex layouts with table extraction and reading-order detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adelpro](https://clawhub.ai/user/adelpro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to convert PDFs into Markdown, JSON, or HTML for RAG pipelines, document parsing, accessibility, data extraction, or content migration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install instructions include a remote script piped directly into bash. <br>
Mitigation: Prefer installing opendataloader-pdf in a virtual environment and Java through a trusted package manager; download, inspect, and verify any remote install script before running it. <br>
Risk: Converted PDF outputs may contain sensitive document content. <br>
Mitigation: Store generated Markdown, JSON, and HTML files in an appropriate local workspace and handle them according to the user's data-sensitivity requirements. <br>


## Reference(s): <br>
- [OpenDataLoader PDF](https://github.com/opendataloader-project/opendataloader-pdf) <br>
- [PDF/UA](https://pdfa.org) <br>
- [veraPDF](https://verapdf.org) <br>
- [ClawHub](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, HTML, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with bash and Python examples for producing Markdown, JSON, or HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Java 11+ and Python 3.10+ with opendataloader-pdf; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
