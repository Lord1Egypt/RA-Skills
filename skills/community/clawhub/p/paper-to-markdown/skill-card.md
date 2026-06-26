## Description: <br>
PDF to Markdown converter - extract text, tables and formulas from PDF files to clean Markdown. Use when converting PDF documents, extracting PDF content, parsing PDF text, or summarizing PDF reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and document analysts use this skill to convert local PDF files or PDF URLs into clean Markdown for extraction, parsing, summarization, or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs or PDF links are sent to MinerU's external service for processing. <br>
Mitigation: Use only documents approved for that external data flow, and avoid private or regulated PDFs unless that processing is acceptable. <br>
Risk: Larger-file or precision extraction may require MinerU authentication. <br>
Mitigation: Run MinerU authentication only when intentionally using the authenticated extraction mode. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tanis90/paper-to-markdown) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU CLI](https://mineru.net/ecosystem?tab=cli) <br>
- [MinerU Project](https://github.com/opendatalab/MinerU) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flash extraction returns Markdown only and is limited to 10MB or 20 pages per document.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
