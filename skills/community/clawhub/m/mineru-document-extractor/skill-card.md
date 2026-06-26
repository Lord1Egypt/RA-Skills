## Description: <br>
MinerU Document Extractor helps agents convert PDFs, scans, images, Office documents, spreadsheets, and web pages into Markdown, HTML, LaTeX, DOCX, JSON, or plain text using the mineru-open-api CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mineru-extract](https://clawhub.ai/user/mineru-extract) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, data engineers, and other external users use this skill to extract readable content, tables, formulas, and OCR text from documents and web pages for downstream analysis or conversion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents, scans, spreadsheets, images, or web pages selected for extraction are sent to MinerU's online service for processing. <br>
Mitigation: Avoid confidential or regulated material unless MinerU's terms and organizational policy allow it. <br>
Risk: A configured MinerU token could expose access if stored or shared carelessly. <br>
Mitigation: Use approved secret handling for MINERU_TOKEN or ~/.mineru/config.yaml, and rotate the token if exposure is suspected. <br>
Risk: VLM-based extraction may produce inaccurate or hallucinated text for complex layouts. <br>
Mitigation: Review extracted content before relying on it, and use the pipeline model when no-hallucination behavior is more important than layout accuracy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mineru-extract/mineru-document-extractor) <br>
- [MinerU CLI reference](https://github.com/opendatalab/MinerU-Ecosystem/tree/main/cli) <br>
- [MinerU API token management](https://mineru.net/apiManage/token) <br>
- [Publisher profile](https://clawhub.ai/user/mineru-extract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; extracted results may be Markdown, HTML, LaTeX, DOCX, JSON, or plain text depending on command options.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require mineru-open-api, MINERU_TOKEN, or ~/.mineru/config.yaml; flash-extract is limited to 10 MB and 20 pages per file.] <br>

## Skill Version(s): <br>
0.1.30 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
