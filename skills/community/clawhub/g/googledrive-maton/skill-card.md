## Description:

Access and manage Google Drive files, folders, metadata, uploads, downloads, and sharing through Maton Gateway with OAuth-backed API access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otman-ai](https://clawhub.ai/user/otman-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill as a cURL reference for connecting agent workflows to Google Drive through Maton Gateway. It covers connection management, file listing and search, uploads, downloads, metadata updates, sharing permissions, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact Google Drive operations can delete files, upload or overwrite content, and change sharing permissions.

Mitigation: Use a narrowly scoped Maton API key and Google Drive connection, confirm exact file or folder IDs, and test read-only operations before running write, delete, upload, or sharing commands.

Risk: Printing the Maton API key can expose credentials in terminal history, logs, or shared screens.

Mitigation: Check only whether MATON_API_KEY is set and avoid echoing or logging secret values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/otman-ai/skills/googledrive-maton)
- [Skill source artifact](artifact/Skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with cURL command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API-key, connection, file, upload, sharing, and troubleshooting examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
