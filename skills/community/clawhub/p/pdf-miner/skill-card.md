## Description: <br>
Extracts text, tables, keywords, metrics, tables of contents, document diffs, and LLM-friendly chunks from PDF files, with optional OCR for low-text scanned pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baichenwzj](https://clawhub.ai/user/baichenwzj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use pdf-miner to convert PDF reports, research papers, and financial documents into readable text, Markdown tables, JSON table data, or chunked files for downstream review and LLM analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF page images can be sent to an external OCR API when automatic OCR is enabled or OCR is requested. <br>
Mitigation: Avoid OCR for confidential PDFs by running with --no-auto-ocr or leaving OCR credentials unconfigured; when OCR is needed, prefer environment variables for credentials and verify the configured endpoint and model before processing sensitive documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baichenwzj/pdf-miner) <br>
- [OpenRouter-compatible OCR API endpoint](https://openrouter.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON table data, or generated files from command-line extraction modes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create extracted Markdown files, JSON table output, chunk files, or batch output directories depending on command options.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
