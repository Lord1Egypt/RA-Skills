## Description:

Convert DocSend document URLs to PDF through Docsend2pdf.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can convert a DocSend document URL into a PDF and receive download metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may make persistent changes to other agent skills.

Mitigation: Review the CLI setup behavior and disable automatic synchronization if only document conversion is needed.

Risk: Conversion requires sharing a document link with OOMOL and Docsend2pdf.

Mitigation: Submit confidential links only when you authorize both services to access them.

Risk: Remote installer contents and hosted processing are unverified.

Mitigation: Review installer contents before running setup and assess the provider's processing practices.

## Reference(s):

- [Docsend2pdf homepage](https://docsend2pdf.com)
- [Docsend2pdf API documentation](https://docsend2pdf.com/api-docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [PDF document with JSON download metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The response includes download metadata.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
