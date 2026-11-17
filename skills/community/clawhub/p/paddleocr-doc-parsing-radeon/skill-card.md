## Description:

PaddleOCR Doc Parsing Radeon extracts structured Markdown and JSON from PDFs and document images using PaddleOCR-VL 1.5 through an AMD Radeon Cloud endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiwork4me](https://clawhub.ai/user/aiwork4me)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and document-processing agents use this skill to parse PDFs and document images into structured text, Markdown, tables, formulas, and layout data. It is best suited for complex documents such as invoices, financial reports, academic papers, charts, and multi-column layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents may be uploaded to a third-party or untrusted parsing endpoint.

Mitigation: Use the skill only with a parsing endpoint you control and trust, and avoid confidential, regulated, financial, personal, or internal documents unless that endpoint is approved for the data.

Risk: The configured endpoint may use unencrypted HTTP, exposing uploaded documents and parser responses to network observers.

Mitigation: Configure PADDLEOCR_DOC_PARSING_API_URL with an HTTPS endpoint before handling sensitive content.

Risk: The --file-url workflow can fetch arbitrary URLs supplied by a user.

Mitigation: Accept URL inputs only from trusted users or approved domains, and prefer local files or pre-vetted URLs in shared environments.

## Reference(s):

- [ClawHub Skill Homepage](https://clawhub.ai/aiwork4me/paddleocr-doc-parsing-radeon)
- [ClawHub Skill Page](https://clawhub.ai/aiwork4me/skills/paddleocr-doc-parsing-radeon)
- [PaddleOCR Document Parsing Output Schema](references/output_schema.md)
- [Original ClawHub PaddleOCR Document Parsing Skill](https://clawhub.ai/bobholamovic/paddleocr-doc-parsing)
- [PEP 723 Inline Script Metadata](https://peps.python.org/pep-0723/)
- [uv Documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON envelope with extracted text, raw parsing results, and errors; agents may present the extracted content as Markdown or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save JSON results to a caller-selected output file; supports URL or local file inputs, PDF/image file type selection, image optimization, and PDF page splitting.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
