## Description:

Automate Inkly eSignature workflows by sending documents, checking signing status, and retrieving completed PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inkly-so](https://clawhub.ai/user/inkly-so)

### License/Terms of Use:

MIT

## Use Case:

External users can use this skill to prepare and manage eSignature workflows with Inkly, including sending documents from templates or PDFs, tracking signing progress, and retrieving completed documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial: two local path-like references were not matched to bundled artifacts, and the review notes an external request.

Mitigation: Review the unresolved references and confirm you trust Inkly before installing. Provide an API key only when needed and do not print or log it.

Risk: Sending or voiding a document has real effects; a sent document emails recipients, and sends and voids cannot be undone.

Mitigation: Prepare a draft by default. Before sending, voiding, or reminding, confirm the document, recipients, and prefilled values with the user.

## Reference(s):

- [Inkly AI agent documentation](https://www.inkly.so/docs/api/ai-agents)
- [Inkly API reference (OpenAPI)](https://www.inkly.so/api/v1/openapi.json)
- [Inkly field markers](https://www.inkly.so/docs/api/field-markers)

## Skill Output:

**Output Type(s):** [Text, Guidance, PDF files]

**Output Format:** [Text responses, review or download links, and signed PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Signing status and document links depend on Inkly API responses; completed PDF download links are temporary.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
