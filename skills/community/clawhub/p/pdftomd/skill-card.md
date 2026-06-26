## Description: <br>
Converts PDF files to clean Markdown by extracting text, tables, and formulas with MinerU Open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert local PDF files or PDF URLs into Markdown for extraction, summarization, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF content or PDF URLs are sent to MinerU for online processing. <br>
Mitigation: Use the skill only when third-party processing is allowed, and avoid confidential, regulated, or highly sensitive documents unless that handling is approved. <br>
Risk: The flash-extract workflow has document size and page limits, and images, tables, or formulas may be replaced with placeholders. <br>
Mitigation: Use the authenticated mineru-open-api extract workflow for larger files or precision extraction with full assets when appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tanis90/pdftomd) <br>
- [MinerU Homepage](https://mineru.net) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU CLI Download](https://mineru.net/ecosystem?tab=cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill invokes mineru-open-api and sends selected PDFs or PDF URLs to MinerU for online processing; flash-extract output is Markdown only.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
