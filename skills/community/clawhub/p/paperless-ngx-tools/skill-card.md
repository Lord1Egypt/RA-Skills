## Description:

Manage documents in Paperless-ngx - search, upload, tag, and retrieve.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madmantim](https://clawhub.ai/user/madmantim)

### License/Terms of Use:


## Use Case:

Developers, operators, and Paperless-ngx users use this skill to let an agent search, list, retrieve, upload, download, and organize documents in a configured Paperless-ngx instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive Paperless-ngx document data and credentials.

Mitigation: Install only for trusted Paperless servers, prefer HTTPS outside strictly local environments, and use a low-privilege Paperless token.

Risk: Full OCR content and downloads can expose sensitive document contents.

Mitigation: Use full-content retrieval only when needed and choose safe, explicit download output paths.

Risk: Advanced API operations can modify or delete Paperless records.

Mitigation: Review delete, bulk-edit, upload, and metadata-creation operations before allowing an agent to run them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/madmantim/skills/paperless-ngx-tools)
- [Paperless-ngx API Reference](references/api.md)
- [Paperless-ngx project](https://github.com/paperless-ngx/paperless-ngx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; helper scripts return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PAPERLESS_URL and PAPERLESS_TOKEN; document search and metadata operations depend on the configured Paperless-ngx server and token permissions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
