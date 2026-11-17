## Description:

Secure Google Sheets Management - permission-based create, read, write, and append spreadsheet data, plus file management (share, permissions, rename, delete).

This skill is ready for commercial/non-commercial use.

## Publisher:

[porteden](https://clawhub.ai/user/porteden)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate PortEden CLI commands for Google Sheets data operations and file management. It supports authenticated workflows for reading, writing, appending, sharing, renaming, downloading links for, and deleting Google Sheets files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running the PortEden CLI requires trust in a third-party command-line tool.

Mitigation: Use a verified or pinned PortEden CLI release when available and confirm the install source before use.

Risk: Google Drive and PE_API_KEY credentials can authorize sensitive spreadsheet access.

Mitigation: Use the narrowest Google scopes and PE_API_KEY permissions that support the task.

Risk: Share, public share, write, and delete commands can expose, alter, or remove spreadsheet data.

Mitigation: Confirm the provider-prefixed file ID, target range, permission recipient, role, and delete intent before executing high-impact commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/porteden/skills/porteden-sheets)
- [PortEden publisher profile](https://clawhub.ai/user/porteden)
- [PortEden homepage](https://porteden.com)
- [PortEden CLI Go module](https://github.com/porteden/cli/cmd/porteden)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-output recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends compact JSON CLI output with the -jc flag when an agent needs structured responses.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
