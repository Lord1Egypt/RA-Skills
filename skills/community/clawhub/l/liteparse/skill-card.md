## Description:

Parse, extract text from, and screenshot PDF and document files locally using the LiteParse CLI (`lit`).

This skill is ready for commercial/non-commercial use.

## Publisher:

[alfred-intel-handler-source](https://clawhub.ai/user/alfred-intel-handler-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use LiteParse to extract text, structured JSON, and page screenshots from PDFs and common office or image document formats for local document-processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LiteParse is a third-party CLI that can read any documents provided to it.

Mitigation: Review and pin the installed package version when supply-chain control matters, and only point the CLI at documents the user intends to process.

Risk: Strict offline operation can be affected by OCR language-data downloads or optional cloud fallback guidance.

Mitigation: Use `--no-ocr` for text-layer PDFs or preinstall OCR language data, and avoid the optional cloud fallback for sensitive documents.

Risk: Complex tables, multi-column layouts, and scanned forms may produce imperfect extracted text.

Mitigation: Inspect outputs before relying on them for critical decisions and use page screenshots or a higher-fidelity parser for difficult layouts.

## Reference(s):

- [LiteParse documentation](https://developers.llamaindex.ai/liteparse/)
- [LlamaParse cloud service](https://cloud.llamaindex.ai)
- [LiteParse output examples](references/output-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and examples of text, JSON, and image-file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local document extraction guidance for the `lit` CLI; parsed documents may produce text, JSON with bounding boxes, or page screenshot files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
