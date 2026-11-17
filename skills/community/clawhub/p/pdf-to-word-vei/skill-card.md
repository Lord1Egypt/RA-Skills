## Description:

Converts PDF documents to Word (.docx) files and guides agents through upload, conversion, status checks, downloads, batch conversion, and conversion history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veilei](https://clawhub.ai/user/veilei)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert PDFs into DOCX documents and manage conversion tasks through a local document-conversion workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated file, download, history, and deletion APIs could expose or modify converted documents if the service is reachable by untrusted users.

Mitigation: Use the service only on localhost or another access-controlled endpoint, and add authentication plus ownership checks before exposing it beyond a single trusted user environment.

Risk: Uploaded PDFs and conversion history may contain sensitive document content or metadata.

Mitigation: Avoid sensitive documents unless storage, retention, and history handling are understood and acceptable for the environment.

## Reference(s):

- [API Reference](references/api.md)
- [System Architecture](references/architecture.md)
- [ClawHub Skill Page](https://clawhub.ai/veilei/skills/pdf-to-word-vei)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with API examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow guidance for document conversion; converted document files are produced by the referenced conversion service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
