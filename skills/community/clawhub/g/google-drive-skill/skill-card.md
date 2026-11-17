## Description:

Enables agents to list, download, create, update, delete, and share Google Drive files and folders using Drive API v3 with API-key read access or service-account write access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dvnghiem](https://clawhub.ai/user/dvnghiem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to integrate Google Drive into scripts or applications, read publicly shared files, manage service-account-owned Drive content, and automate folder structures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A download path can overwrite local files, especially when downloading untrusted Drive files into a directory.

Mitigation: Download into a dedicated directory, check the resolved destination before execution, and avoid trusting remote filenames for sensitive paths.

Risk: Read-only commands may still use full Drive credentials when service-account credentials are present.

Mitigation: Use an API key for public read-only access where possible, and unset service-account credentials in read-only runs.

Risk: Public sharing, writer roles, and non-interactive permanent deletion can expose or destroy Drive content.

Mitigation: Review file IDs and permission roles before execution, prefer trashing over permanent deletion, and audit sharing after permission changes.

Risk: Broad service-account credentials can grant more Drive access than a task needs.

Mitigation: Use a tightly scoped service account and keep credential files outside the repository or in a secret manager.

## Reference(s):

- [Google Drive MIME Types Reference](references/mime_types.md)
- [Google Drive Errors Reference](references/error_codes.md)
- [Service Account Template](assets/service_account_template.json)
- [Drive API v3 documentation](https://developers.google.com/drive/api/v3/reference)
- [Python client library for Drive v3](https://googleapis.github.io/google-api-python-client/docs/dyn/drive_v3.html)
- [Service accounts guide](https://developers.google.com/identity/protocols/oauth2/service-account)
- [Drive MIME types](https://developers.google.com/drive/api/guides/mime-types)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command patterns for Google Drive API operations and may guide creation or handling of local files when scripts are executed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
