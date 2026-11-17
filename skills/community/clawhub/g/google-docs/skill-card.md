## Description:

Guides agents in accessing Google Docs to read, create, and edit documents with user-authorized access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to retrieve Google Docs content and, with approval, create or update documents and formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an account may grant access to sensitive documents.

Mitigation: Confirm the account and documents needed; use read-only scopes where possible.

Risk: Document edits or new connections can change data or access.

Mitigation: Confirm the target and intended effect before each write or connection.

Risk: Hosted functions, triggers, and destinations can create ongoing access or forwarding.

Mitigation: Review and separately approve each automation, destination, and recipient before enabling it.

Risk: Raw API keys can expose access if mishandled.

Mitigation: Prefer the authenticated CLI and avoid exposing or logging API keys.

## Reference(s):

- [ClawHub Google Docs skill](https://clawhub.ai/byungkyu/skills/google-docs)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Google Docs API overview](https://developers.google.com/docs/api/how-tos/overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline commands and document content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Document content and metadata may be sensitive; edits require user confirmation.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
