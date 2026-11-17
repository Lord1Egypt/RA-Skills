## Description:

Upload and categorize documents using the Paperless-ngx API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thistine](https://clawhub.ai/user/thistine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to upload documents to a Paperless-ngx instance and attach titles, tags, or document types for document-management automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document uploads and API tokens may be exposed if used with unsafe transport settings or an untrusted Paperless-ngx server.

Mitigation: Use only a Paperless-ngx server you control, prefer HTTPS with valid certificate verification, and confirm the destination before uploading sensitive documents.

Risk: API keys can leak through command history, logs, or shared prompts.

Mitigation: Avoid placing real API keys directly in command history or shared prompts; use local secret handling where possible.

## Reference(s):

- [Paperless-ngx API Endpoints](references/api_endpoints.md)
- [ClawHub Skill Page](https://clawhub.ai/thistine/skills/paperless-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, Paperless-ngx host URL, API token handling guidance, and document metadata such as title, tags, and document type.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
