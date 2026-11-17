## Description:

Pdf Field Extractor helps an agent extract structured fields from PDFs, including invoices, contracts, receipts, bank statements, licenses, ID documents, shipping forms, and generic documents, with Excel or JSON outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiji0802](https://clawhub.ai/user/qiji0802)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn user-provided PDFs into structured records for review, export, and downstream workflow automation. It is suited for document intake tasks where fields must be extracted from text PDFs or OCR-processed scanned PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive PDF contents may be sent to the configured model endpoint during field extraction.

Mitigation: Use only trusted HTTPS endpoints and process identity, banking, or confidential business documents only when the data-handling requirements allow remote AI processing.

Risk: API keys may be exposed to a configurable outside endpoint if endpoint settings are untrusted.

Mitigation: Avoid custom or untrusted api_base values and do not reuse an API key with unrelated providers.

Risk: Generated Excel or JSON outputs may contain sensitive or incorrect extracted fields.

Mitigation: Review generated files before sharing or using them in downstream workflows.

## Reference(s):

- [Document Type Identification Reference](artifact/references/doc_types.md)
- [AI Field Extraction Prompt Templates](artifact/references/prompts.md)
- [Tier Configuration](artifact/scripts/tier_config.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python snippets; extraction results may be written as Excel (.xlsx) or JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-configured model credentials and endpoint settings; OCR may be used for scanned PDFs.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
