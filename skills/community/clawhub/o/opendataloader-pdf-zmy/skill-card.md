## Description:

OpenDataLoader PDF parses PDFs into Markdown, JSON, HTML, or text for RAG pipelines, table extraction with bounding boxes, OCR workflows, and AI-enriched descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert PDFs into LLM-ready text, Markdown, JSON, or HTML for knowledge bases, citation-aware extraction, and RAG pipelines. It is especially relevant for structured PDFs such as reports, academic papers, invoices, scanned documents, and medical-style records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive PDF content may be exposed when converted text is sent to remote, AI-backed, or embedding services.

Mitigation: Treat converted PDF content as sensitive, use localhost or trusted authenticated hybrid backends, and review third-party embedding use before processing confidential documents.

Risk: Untrusted PDFs can introduce prompt-injection content into downstream RAG or agent workflows.

Mitigation: Enable sanitization for untrusted PDFs and review extracted content before indexing it or passing it to an LLM.

Risk: Pointing OPENDATALOADER_HYBRID_URL at an untrusted service can expose source documents or extracted text.

Mitigation: Keep OPENDATALOADER_HYBRID_URL on localhost or a trusted authenticated backend.

## Reference(s):

- [API Reference](references/api-reference.md)
- [CLI Reference](references/cli-reference.md)
- [Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/zmy1006-sudo/skills/opendataloader-pdf-zmy)
- [Publisher Profile](https://clawhub.ai/user/zmy1006-sudo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes usage patterns for local parsing, hybrid parsing, OCR, sanitization, and downstream RAG workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
