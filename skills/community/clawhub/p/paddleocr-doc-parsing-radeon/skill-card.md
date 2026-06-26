## Description: <br>
Parses PDFs and document images with PaddleOCR-VL 1.5 on an AMD Radeon Cloud endpoint to extract structured text, Markdown, JSON, tables, formulas, figures, and reading order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiwork4me](https://clawhub.ai/user/aiwork4me) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to parse selected PDFs or document images into structured content for extraction, review, search indexing, RAG, and downstream document workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents or fetched URLs are sent to the configured PaddleOCR/Radeon Cloud endpoint. <br>
Mitigation: Use a trusted HTTPS endpoint and avoid submitting confidential documents unless its retention, logging, and access practices are acceptable. <br>
Risk: Document parsing can be incomplete or inaccurate for complex layouts, low-quality scans, unsupported formats, or large files. <br>
Mitigation: Review extracted text, tables, formulas, confidence values, and errors before relying on the output in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aiwork4me/paddleocr-doc-parsing-radeon) <br>
- [PaddleOCR Document Parsing Output Schema](references/output_schema.md) <br>
- [uv Documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON envelope with extracted text and page-level Markdown; optional saved JSON file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output may include raw provider response data, layout regions, table structure, formulas, figures, confidence values, and error details.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
