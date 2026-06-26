## Description: <br>
Complex document parsing with PaddleOCR. Intelligently converts complex PDFs and document images into Markdown and JSON files that preserve the original structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sfresurgam](https://clawhub.ai/user/sfresurgam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to parse complex PDFs and document images through a configured PaddleOCR/Triton endpoint, then return extracted text, Markdown, and structured JSON for documents with tables, formulas, figures, charts, and multi-column layouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents are sent to the configured PaddleOCR/Triton endpoint. <br>
Mitigation: Use a trusted local or internal endpoint for sensitive documents and confirm PADDLEOCR_DOC_PARSING_API_URL before processing. <br>
Risk: Raw document-parsing results may be saved locally by default. <br>
Mitigation: Use --stdout or a controlled --output path when persistence is not desired, and delete saved JSON results when they are no longer needed. <br>
Risk: Passing untrusted document URLs to the backend can expose the endpoint to unwanted network retrievals. <br>
Mitigation: Avoid untrusted URLs and prefer vetted local files or trusted document-hosting locations. <br>


## Reference(s): <br>
- [Output Schema](references/output_schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sfresurgam/paddleocr-vl-locally) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with command examples and JSON document-parsing envelopes saved to files or printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The JSON envelope includes ok, text, result, and error fields; saved results default to the system temp directory unless --output or --stdout is used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
