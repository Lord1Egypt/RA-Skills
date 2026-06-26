## Description: <br>
Uses the MinerU API to convert local or online PDFs into Markdown with formula, table, OCR, and multilingual extraction support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alex-ZxYz](https://clawhub.ai/user/Alex-ZxYz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to parse academic papers and other PDF documents into Markdown for document extraction, review, and knowledge-base construction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF content and the MINERU_TOKEN are sent to MinerU for processing. <br>
Mitigation: Use the skill only with documents approved for MinerU processing and only when you trust MinerU with the token and submitted PDFs. <br>
Risk: Parsed documents are saved locally under ~/.openclaw/MinerU_Results. <br>
Mitigation: Review and clean up local output files according to the sensitivity and retention requirements for the processed documents. <br>
Risk: Automatic paper-workflow invocation can process sensitive, regulated, or internal documents unintentionally. <br>
Mitigation: Disable or avoid automatic invocation for sensitive workflows unless the document handling has been approved. <br>


## Reference(s): <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>
- [ClawHub skill page](https://clawhub.ai/Alex-ZxYz/mineru-pdf-parser) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINERU_TOKEN, sends selected PDFs or PDF URLs to MinerU, and saves parsed results under ~/.openclaw/MinerU_Results.] <br>

## Skill Version(s): <br>
3.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
