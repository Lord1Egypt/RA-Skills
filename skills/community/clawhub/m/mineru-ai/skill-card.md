## Description: <br>
MinerU Doc Parser helps agents convert PDFs, scanned documents, images, Office files, and web pages into structured Markdown or other document formats using the MinerU CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mineru-extract](https://clawhub.ai/user/mineru-extract) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, data scientists, and document-processing teams use this skill to run MinerU document extraction, OCR, table and formula recognition, batch conversion, and web-page crawling from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send local documents, images, or URLs to MinerU/OpenDataLab services for parsing. <br>
Mitigation: Use it only with documents and URLs approved for that external data flow, and avoid confidential or regulated files unless the service path has been reviewed. <br>
Risk: Broad document-parsing activation triggers can make remote extraction feel routine before the data-sharing implication is obvious. <br>
Mitigation: Confirm the source file or URL and the selected extraction mode before running mineru-open-api, especially for private documents or intranet URLs. <br>
Risk: Generated output directories may contain extracted text, images, or converted documents with sensitive content. <br>
Mitigation: Review, protect, or clean generated output directories after use according to the sensitivity of the source material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mineru-extract/mineru-ai) <br>
- [Publisher profile](https://clawhub.ai/user/mineru-extract) <br>
- [MinerU homepage](https://mineru.net) <br>
- [OpenClaw source metadata](https://github.com/MinerU-Extract/mineru-ai) <br>
- [MinerU Ecosystem CLI reference](https://github.com/opendatalab/MinerU-Ecosystem/tree/main/cli) <br>
- [Skill overview](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and CLI output paths; executed commands may produce Markdown, HTML, LaTeX, DOCX, JSON, and extracted image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the mineru-open-api binary; flash extraction is limited to 10 MB and 20 pages, while precision extraction and crawling require a MinerU token.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
