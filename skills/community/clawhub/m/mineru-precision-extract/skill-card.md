## Description: <br>
MinerU precision extract converts PDFs, scanned documents, images, Word, PowerPoint, and HTML files into Markdown, HTML, LaTeX, DOCX, or JSON with table recognition, formula recognition, OCR, batch processing, and web crawling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mineru-extract](https://clawhub.ai/user/mineru-extract) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, data engineers, and document-processing teams use this skill to guide high-accuracy extraction, OCR, table recognition, formula recognition, batch conversion, and web-to-Markdown workflows through the MinerU CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a MinerU API token and can expose credentials if tokens are copied into logs, screenshots, shared scripts, or source control. <br>
Mitigation: Use the documented auth flow or environment variable handling, keep tokens out of command transcripts and repositories, and rotate any token that may have been exposed. <br>
Risk: Documents, remote files, and crawled URLs may be processed by an external MinerU service. <br>
Mitigation: Only process confidential documents, private URLs, or internal web pages when MinerU/OpenDataLab and the deployment are approved for that data. <br>
Risk: Wildcard, batch, or list-based commands can process more files or URLs than intended. <br>
Mitigation: Review expanded inputs and file lists before execution, especially when using wildcards, batch directories, or URL lists. <br>


## Reference(s): <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU precision extract source](https://github.com/MinerU-Extract/mineru-precision-extract) <br>
- [MinerU Ecosystem CLI](https://github.com/opendatalab/MinerU-Ecosystem/tree/main/cli) <br>
- [MinerU document extractor](https://github.com/MinerU-Extract/mineru-document-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to produce MinerU CLI commands and configuration steps; the CLI can produce Markdown, HTML, LaTeX, DOCX, or JSON outputs from supported documents.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
