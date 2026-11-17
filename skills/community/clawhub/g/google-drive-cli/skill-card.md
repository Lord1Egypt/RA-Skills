## Description:

Interact with Google Drive, Docs, and Sheets using the drivectl CLI for listing Drive files, downloading files, reading or updating Sheets, and creating or exporting Google Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghchinoy](https://clawhub.ai/user/ghchinoy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to guide an agent in running drivectl commands for Google Drive, Docs, and Sheets tasks, including structured JSON output for programmatic parsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and authenticate a broad native CLI for Google Workspace.

Mitigation: Review before installing, use only a trusted drivectl release, and prefer a pinned and independently verified binary.

Risk: Authenticated commands can create, update, delete, export, or share Workspace content, including dynamic API calls outside Drive, Docs, and Sheets.

Mitigation: Authenticate with least-privilege OAuth scopes and require explicit confirmation before state-changing, export, sharing, or dynamic API actions.

Risk: The bundled installer may continue without checksum validation if no supported checksum utility is available.

Mitigation: Install checksum tooling or independently verify the downloaded binary before using it with Google Workspace credentials.

## Reference(s):

- [Google Drive Operations](references/drive.md)
- [Google Docs Operations](references/docs.md)
- [Google Sheets Operations](references/sheets.md)
- [Dynamic API Discovery](references/discovery.md)
- [Google Drive API v3 Discovery Document](https://www.googleapis.com/discovery/v1/apis/drive/v3/rest)
- [ClawHub Skill Page](https://clawhub.ai/ghchinoy/skills/google-drive-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should use -O json when structured output is needed.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
