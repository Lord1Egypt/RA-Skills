## Description: <br>
Summarizes academic paper PDFs into Feishu documents with structured Markdown, selected figures, duplicate checks, and reviewer-assisted data verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yy-fan](https://clawhub.ai/user/yy-fan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical readers use this skill to turn academic PDFs or technical reports into Feishu summaries with structured sections, selected figures, duplicate checks, and review before final confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF-derived text and selected figures may be written to Feishu and processed by sub-agents. <br>
Mitigation: Use this skill only when Feishu storage and sub-agent processing are acceptable; avoid confidential or unpublished PDFs unless that handling is approved. <br>
Risk: The workflow may require installing local system packages for PDF extraction, OCR, and JSON processing. <br>
Mitigation: Review and approve any installation of poppler-utils, tesseract-ocr, and jq before execution. <br>
Risk: Local paper folders, logs, extracted text, image files, and Feishu token files may remain after processing. <br>
Mitigation: Delete local paper folders, logs, extracted files, and token files after completion, especially for sensitive papers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yy-fan/paper-summarize-pdf-to-feishu) <br>
- [Summary template](references/summary_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local paper folders, logs, metadata JSON, extracted text and images, summaries, audit reports, and Feishu document content when the required tools are available.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
