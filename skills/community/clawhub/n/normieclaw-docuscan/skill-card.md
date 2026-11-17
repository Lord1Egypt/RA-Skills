## Description:

DocuScan turns photos of receipts, contracts, whiteboards, and handwritten notes into reconstructed searchable documents and PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT

## Use Case:

Developers and end users use DocuScan to extract text and structure from document photos, reconstruct Markdown, and generate local searchable PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanned documents can contain sensitive personal, financial, medical, or legal data stored in the local workspace.

Mitigation: Restrict access to the documents directory, use private storage and encryption for any dashboard, and avoid processing documents unless local handling is acceptable.

Risk: PDF generation may expose local files or render unsafe document-derived HTML if inputs are not tightly constrained.

Mitigation: Permit only validated input files and approved assets under documents, escape or reject raw HTML from extracted text, and use pinned Playwright/Chromium dependencies in a virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-docuscan)
- [README](README.md)
- [Security guidance](SECURITY.md)
- [PDF templates](config/pdf-templates.md)
- [Dashboard companion kit](dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with optional local HTML/PDF files and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores generated documents under documents/ and may update documents/scan-log.json.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
