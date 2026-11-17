## Description:

Extracts text and tables from PDFs, with modes for keyword search, metric extraction, table-of-contents detection, PDF comparison, chunking, batch processing, and header/footer cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baichenwzj](https://clawhub.ai/user/baichenwzj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to extract readable Markdown or JSON from PDF reports, papers, and financial documents when ordinary web fetchers or simple PDF parsers are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Low-text PDF pages can be rendered and sent to a configured external vision API when OCR is available, which may expose confidential document content.

Mitigation: Review before installing, use --no-auto-ocr or selective OCR for sensitive PDFs, approve any remote OCR provider before use, and avoid storing API keys in config.json.

Risk: The top-level skill description says OCR is not in scope, while the artifact can trigger automatic OCR for low-text pages.

Mitigation: Treat OCR behavior as active unless disabled, and document this behavior for users who expect extraction-only PDF processing.

## Reference(s):

- [OpenRouter-compatible vision API endpoint](https://openrouter.ai/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown extraction files, optional JSON table output, and shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write extracted pages, tables, search results, metrics, TOC entries, diffs, or chunks to files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
