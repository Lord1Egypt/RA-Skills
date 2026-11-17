## Description:

Provides agent guidance for managing Google Drive files and folders through the PortEden CLI, including listing, searching, reading text content, creating, uploading, sharing, moving, renaming, and deleting items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porteden](https://clawhub.ai/user/porteden)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill through an agent to manage Google Drive files and folders via the PortEden CLI, especially when they need compact command output for Drive listing, reading, creation, upload, folder management, sharing, permission review, move, rename, or trash workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party CLI with access to Google Drive data and account scopes.

Mitigation: Install only if the publisher and granted scopes are trusted; prefer a restricted Google account or token for sensitive use.

Risk: Sharing and delete workflows can expose files or move Drive items to trash.

Mitigation: Review sharing, permission, and delete requests carefully before execution.

Risk: CLI version or package source changes could affect behavior when handling sensitive Drive content.

Mitigation: Pin or otherwise verify the PortEden CLI version before use in sensitive environments.

## Reference(s):

- [PortEden homepage](https://porteden.com)
- [ClawHub skill page](https://clawhub.ai/porteden/skills/google-drive-secured)
- [PortEden publisher profile](https://clawhub.ai/user/porteden)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PortEden CLI commands and recommends compact JSON output with -jc where available.]

## Skill Version(s):

1.0.8 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
