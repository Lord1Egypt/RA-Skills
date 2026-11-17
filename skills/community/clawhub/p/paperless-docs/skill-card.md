## Description:

Manage documents in Paperless-ngx - search, upload, tag, and retrieve.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madmantim](https://clawhub.ai/user/madmantim)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect an agent to a configured Paperless-ngx instance so it can search, list, retrieve, upload, download, and organize documents through helper commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Paperless API token can allow broad access to document data, especially when used with an untrusted server or non-HTTPS URL.

Mitigation: Configure only trusted Paperless servers, prefer HTTPS, and use a least-privilege Paperless token.

Risk: The skill can read, upload, download, and modify Paperless document data using the configured token.

Mitigation: Review requested operations before execution and scope the Paperless account or token to the minimum permissions needed.

Risk: Downloaded files can overwrite local paths or place sensitive documents in unintended locations.

Mitigation: Specify safe download output paths and review destination filenames before running downloads.

Risk: Full document content retrieval can expose sensitive or very large OCR text.

Mitigation: Avoid full-content retrieval for sensitive or very large documents unless it is necessary.

## Reference(s):

- [Paperless-ngx API Reference](artifact/references/api.md)
- [Paperless-ngx Project](https://github.com/paperless-ngx/paperless-ngx)
- [ClawHub Skill Page](https://clawhub.ai/madmantim/skills/paperless-docs)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Files, Configuration guidance]

**Output Format:** [JSON from Node.js helper scripts, with Markdown command examples and configuration snippets in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PAPERLESS_URL and PAPERLESS_TOKEN; download operations can write files to the selected output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
