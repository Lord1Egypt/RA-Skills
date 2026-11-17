## Description:

PasteClaw helps agents create, update, group, and delete text or code snippets through the Pasteclaw.com API and return preview URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tairov](https://clawhub.ai/user/tairov)

### License/Terms of Use:


## Use Case:

Developers, engineers, and external agent users use PasteClaw to publish shareable snippets, demos, documents, notes, and data samples from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may upload secrets, private source code, proprietary documents, personal data, or production configuration to a public Pasteclaw service.

Mitigation: Require explicit review and approval before upload, and do not use the skill for sensitive content.

Risk: The documented curl examples use -sk, which disables TLS certificate verification.

Mitigation: Use certificate-verifying requests instead of the documented -sk examples.

Risk: Optional metadata, session keys, edit tokens, or delete requests can expose trace data or alter published snippets.

Mitigation: Omit optional metadata unless needed, keep tokens and session keys out of URLs, and require confirmation before updates or deletes.

## Reference(s):

- [ClawHub PasteClaw Skill Page](https://clawhub.ai/tairov/skills/pasteclaw)
- [Pasteclaw Service](https://pasteclaw.com)
- [Pasteclaw Snippets API](https://pasteclaw.com/api/snippets)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples, shell commands, and preview URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Pasteclaw snippet IDs, preview URLs, edit tokens, session keys, HTTP status guidance, and optional metadata headers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
