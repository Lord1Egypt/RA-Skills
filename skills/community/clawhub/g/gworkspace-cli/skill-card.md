## Description:

Interact with Google Workspace (Drive, Docs, Sheets) via the `gw` CLI so an agent can browse, read, create, search, or manage Google Drive files, Docs, and Sheets from the terminal across My Drive and Shared Drives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinsadeghpour](https://clawhub.ai/user/robinsadeghpour)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to operate Google Drive, Docs, and Sheets through the `gw` command-line interface. It supports authenticated browsing, reading, creating, uploading, appending, and writing Workspace content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned global third-party CLI that can access persistent OAuth tokens and modify Drive, Docs, and Sheets content.

Mitigation: Review the npm package and source before installing, prefer a pinned reviewed version, and require explicit confirmation before creating, uploading, appending, or writing Workspace content.

Risk: Workspace OAuth tokens, client secrets, config files, and `.env` files are sensitive credentials.

Mitigation: Authenticate with the least Google Workspace access practical and protect `~/.11x/gworkspace/token.json`, `~/.11x/gworkspace/config.json`, client secrets, and environment files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robinsadeghpour/skills/gworkspace-cli)
- [Source repository](https://github.com/robinfaraj/gworkspace-cli)
- [Publisher profile](https://clawhub.ai/user/robinsadeghpour)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to use `gw` commands whose command output may be JSON, tables, IDs, text, Markdown, or tabular data depending on CLI flags.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
