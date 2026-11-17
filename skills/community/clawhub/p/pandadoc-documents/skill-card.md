## Description:

Create and manage PandaDoc documents, templates, folders, and contacts via the PandaDoc API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and developers use this skill to create PandaDoc documents from templates or file uploads, manage templates, folders, contacts, and attachments, and track or send documents for signature through a connected PandaDoc account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes PandaDoc OAuth access through ClawLink, which may expose sensitive document and account access to a third-party integration path.

Mitigation: Install only after confirming the plugin publisher and version, reviewing requested PandaDoc permissions, and granting the least-privileged PandaDoc access available.

Risk: Write actions can send documents, delete templates or contacts, upload attachments, or create webhooks that affect external parties or account state.

Mitigation: Require explicit user confirmation before create, update, delete, send, upload, or webhook actions, including the target resource and intended effect.

## Reference(s):

- [PandaDoc API Documentation](https://developers.pandadoc.com/)
- [PandaDoc Document API](https://developers.pandadoc.com/reference/documents)
- [PandaDoc Template API](https://developers.pandadoc.com/reference/templates)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=pandadoc-documents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool-call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include PandaDoc identifiers, document metadata, contact details, and workflow status from the connected account.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
