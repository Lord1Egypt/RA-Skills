## Description:

Converts text-based or scanned PDFs into structured Markdown and prints a token-usage comparison report for AI reading, archiving, or knowledge-base ingestion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyan521](https://clawhub.ai/user/shiyan521)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and engineers use this skill to convert PDFs such as reports, filings, papers, ebooks, and scanned documents into Markdown before feeding the content to AI systems or storing it in document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic OCR path may render scanned PDF pages to images and send them to an external vision service through a configured adapter.

Mitigation: Use --ocr none for sensitive PDFs unless the OCR path and destination service are explicitly trusted.

Risk: A BAILIAN_ADAPTER environment value or --bailian-adapter argument can cause the skill to load local adapter code.

Mitigation: Set adapter paths only to code that has been inspected and is trusted.

Risk: The documented summary mode does not reduce converted content.

Mitigation: Do not rely on summary mode for content minimization; use token-estimate mode first when scoping cost or exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shiyan521/skills/pdf2md-universal)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown file plus plain-text token comparison report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in token-estimate mode without writing converted content; scanned-PDF OCR may depend on a configured adapter or tesseract.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
