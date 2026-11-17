## Description:

Helps agents use OpenDataLoader PDF to extract and process PDF content for RAG, embeddings, OCR, and coordinate-based citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[secondport](https://clawhub.ai/user/secondport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert PDFs into structured JSON and Markdown for LLM reading, RAG, citations, table extraction, and OCR workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading the external opendataloader-pdf package without source or version verification can introduce supply-chain risk.

Mitigation: Verify package source and metadata, use an isolated environment or container, pin versions, and freeze dependencies before production use.

Risk: Processing sensitive PDFs through the hybrid backend can expose document content if the service is reachable beyond the local machine.

Mitigation: Bind the hybrid backend to localhost when processing sensitive PDFs and verify active listeners before use.

Risk: Extracted JSON, Markdown, images, OCR content, and bounding boxes may contain sensitive source document data.

Mitigation: Store outputs in run-specific folders with appropriate retention and access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/secondport/skills/pdf-extract-skill)
- [OpenDataLoader](https://opendataloader.org/)
- [OpenDataLoader documentation](https://opendataloader.org/docs)
- [Quickstart CLI](docs/quickstart-cli.md)
- [Hybrid Mode and OCR](docs/hybrid-mode-ocr.md)
- [RAG and Citations](docs/rag-citations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; extracted PDF outputs are typically JSON and Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce run-specific output folders containing converted PDF text, metadata, bounding boxes, images, and OCR-derived content.]

## Skill Version(s):

0.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
