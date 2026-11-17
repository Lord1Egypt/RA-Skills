## Description:

Llamaparse parses documents with the LlamaParse API into LLM-ready markdown, text, structured items, metadata, and related outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zli484](https://clawhub.ai/user/zli484)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to parse PDFs, images, spreadsheets, presentations, and scanned documents through LlamaCloud for RAG preparation, OCR, table extraction, chart extraction, and batch document processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents submitted for parsing are uploaded to LlamaCloud, which can expose confidential, regulated, customer, legal, financial, or proprietary content to an external service.

Mitigation: Review document sensitivity before use, avoid regulated or confidential inputs unless the provider relationship permits it, and restrict batch inputs to approved folders.

Risk: Batch parsing can send local path metadata to the provider through the external file identifier.

Mitigation: Use non-sensitive directory and file names for batch runs, or sanitize paths before processing sensitive collections.

Risk: Screenshot saving retrieves files from provider-issued presigned URLs and can create additional local copies of document page images.

Mitigation: Use --save-screenshots only when screenshots are required and store the resulting files in approved locations with appropriate retention controls.

## Reference(s):

- [LlamaParse API Reference](references/api-reference.md)
- [LlamaCloud](https://cloud.llamaindex.ai)
- [LlamaIndex Cloud Documentation](https://developers.llamaindex.ai/python/cloud/)
- [LlamaIndex API Reference](https://developers.api.llamaindex.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; helper scripts can write markdown, text, and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LLAMA_CLOUD_API_KEY and python3; parsed outputs depend on the selected LlamaParse expand views.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
