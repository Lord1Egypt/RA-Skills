## Description: <br>
Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown. Use when extracting content from Word documents, PowerPoint presentations, or Excel spreadsheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract readable Markdown from Office documents and document URLs for summarization, analysis, or content reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected Office documents or document URLs are uploaded to MinerU's external cloud service for processing. <br>
Mitigation: Use the skill only with files you are permitted to send to MinerU, and avoid confidential, regulated, credential-bearing, or internal documents unless that use is approved. <br>
Risk: The unauthenticated flash-extract path is limited to 10MB or 20 pages per document. <br>
Mitigation: Split larger files or use MinerU's authenticated extract flow when larger limits or precision extraction are required. <br>
Risk: Embedded images may be represented as placeholders in the Markdown output. <br>
Mitigation: Review extracted Markdown against the source file when image content matters. <br>


## Reference(s): <br>
- [MinerU](https://mineru.net) <br>
- [MinerU CLI Download](https://mineru.net/ecosystem?tab=cli) <br>
- [ClawHub Skill Page](https://clawhub.ai/tanis90/pptx-to-markdown) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown content and CLI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The flash-extract flow supports DOCX, PPTX, XLS, and XLSX files up to 10MB or 20 pages; embedded images may be returned as placeholders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
