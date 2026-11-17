## Description:

Google Drive API integration with managed OAuth for listing, searching, creating, and managing files and folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprinterx69](https://clawhub.ai/user/sprinterx69)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to interact with Google Drive through Maton-managed OAuth, including file discovery, metadata updates, downloads, uploads, folder operations, and sharing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform broad Google Drive read, write, delete, upload, export, and sharing operations through a third-party gateway.

Mitigation: Install only if Maton is trusted for Google Drive access, require exact file IDs or names plus explicit confirmation before destructive or sharing actions, and revoke unused Google Drive connections when finished.

Risk: The skill relies on MATON_API_KEY, and exposed API keys can allow unauthorized gateway access.

Mitigation: Keep MATON_API_KEY in the environment or a secret manager, do not print or log it, and rotate the key immediately if it appears in logs, screenshots, or shared transcripts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sprinterx69/skills/googledrive)
- [Google Drive API overview](https://developers.google.com/drive/api/reference/rest/v3)
- [Google Drive files.list](https://developers.google.com/drive/api/reference/rest/v3/files/list)
- [Google Drive upload guide](https://developers.google.com/drive/api/guides/manage-uploads)
- [Google Drive search query syntax](https://developers.google.com/drive/api/guides/search-files)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and Python or JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, and an active Google Drive OAuth connection.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
