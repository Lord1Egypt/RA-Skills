## Description:

Connects agents to self-hosted Immich instances for managing photos, albums, users, search, uploads, downloads, libraries, and jobs through the REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninjazan420](https://clawhub.ai/user/ninjazan420)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to automate photo-management workflows against self-hosted Immich deployments, including album management, media upload and download, user lookups, search, library scans, and job operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts accept Immich API keys and may expose credentials through command history or process listings when --api-key is used.

Mitigation: Use narrowly scoped Immich API keys and prefer environment variables or an interactive secret prompt over passing secrets as command-line arguments.

Risk: API calls can upload, download, modify, or delete media and account-related data on the target Immich instance.

Mitigation: Review generated requests before execution, use least-privilege credentials where available, and confirm destructive operations with the user.

Risk: The album download helper writes filenames from server responses into the selected output directory.

Mitigation: Avoid the download helper until album and filename path handling is sanitized and contained to the chosen output directory.

Risk: Connections to an Immich server may transmit private media metadata or files over the network.

Mitigation: Require HTTPS except for explicitly trusted local testing environments.

## Reference(s):

- [Immich API Endpoints Reference](references/api-endpoints.md)
- [ClawHub skill page](https://clawhub.ai/ninjazan420/skills/immich-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python script usage examples, and REST API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run helper scripts that call a user-supplied Immich server and read or write local media files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
