## Description: <br>
Complete local PDF toolkit - OCR, merge, split, compress, watermark, convert, and 30+ operations via the Stirling-PDF API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wudi488](https://clawhub.ai/user/wudi488) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and document-automation users use this skill to configure and call a trusted Stirling-PDF instance for OCR, conversion, merging, compression, watermarking, encryption, and related PDF operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive PDFs, passwords, API keys, and signing material are sent to the configured Stirling-PDF server. <br>
Mitigation: Use only a local or trusted private Stirling-PDF server, keep API keys in environment variables, and avoid public or unknown endpoints. <br>
Risk: One included helper script defaults to an HTTP private-network address that may not be the intended server. <br>
Mitigation: Prefer the localhost-based helper or explicitly set the Stirling-PDF endpoint after reviewing the script defaults. <br>
Risk: The server security verdict is suspicious because a script can send sensitive PDFs to an unexpected hard-coded address. <br>
Mitigation: Review and adjust endpoint configuration before processing confidential documents or passwords. <br>


## Reference(s): <br>
- [Stirling-PDF project repository](https://github.com/Stirling-Tools/Stirling-PDF) <br>
- [ClawHub skill page](https://clawhub.ai/wudi488/local-pdf-suite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, API endpoint examples, and generated file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce processed PDFs, ZIP archives, DOCX, HTML, Markdown, CSV, EPUB, TXT, or JSON error responses from the configured Stirling-PDF server.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
