## Description:

Guides agents through integrating with PDF API Hub REST APIs for HTML/URL-to-PDF generation and related document automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to implement PDF API Hub calls for converting HTML or URLs into PDFs and for related document workflows such as merge, split, OCR, watermarking, signing, locking, and file management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the documented API with real files, URLs, or content sends that data to pdfapihub.com.

Mitigation: Confirm authorization to share the selected documents and review the service's retention and deletion expectations before running adapted examples.

Risk: Copied examples may involve API keys, passwords, signatures, or extracted document data.

Mitigation: Store secrets in environment variables or a secrets manager, avoid committing them, and review outputs before sharing them.

Risk: Delete, unlock, signing, and encryption workflows can affect document access or availability.

Mitigation: Confirm target files, permissions, and intended effects before executing adapted workflow code.

Risk: Hosted output URLs may expire or become unavailable.

Mitigation: Download or persist generated files promptly when long-term access is required.

## Reference(s):

- [PDF API Hub Documentation](https://pdfapihub.com/docs)
- [PDF API Hub Homepage](https://pdfapihub.com/)
- [ClawHub Skill Page](https://clawhub.ai/rishabhdugar/skills/pdf-api-hub)
- [Endpoint Reference](artifact/endpoints.md)
- [Code Examples](artifact/examples.md)
- [Advanced Workflows](artifact/advanced.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with REST API guidance and cURL, Python, and Node.js examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; examples require a PDF API Hub API key and user-selected document URLs or content.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
