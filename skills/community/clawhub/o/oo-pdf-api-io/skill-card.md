## Description:

Use PDF-API.io to list and inspect templates and render PDFs with supplied data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this skill with an OOMOL-connected account to find and inspect PDF-API.io templates, then render PDFs from structured data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can install additional persistent agent skills, and the installer's exact behavior has not been verified.

Mitigation: Review the CLI's additional skill installation and install it separately from a verified release.

Risk: PDF rendering sends document data through OOMOL to PDF-API.io and returns a hosted PDF URL.

Mitigation: Explicitly authorize PDF rendering and the document data sent to OOMOL and PDF-API.io.

## Reference(s):

- [PDF-API.io](https://pdf-api.io)
- [PDF-API.io API documentation](https://www.pdf-api.io/en/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON inputs and PDF-API.io responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rendering returns a temporary hosted PDF URL.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
