## Description:

Helps agents manage OneDrive files, folders, and sharing through a user-authorized Microsoft Graph connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to have an agent find, upload, download, organize, and share files in their authorized OneDrive account. It also documents optional scheduled or event-driven automation through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A connected account may expose sensitive files or permit broader access than the task requires.

Mitigation: Authorize only the required account and scopes; prefer OAuth and read-only access when sufficient.

Risk: Writes, deletions, or anonymous sharing links may change data or disclose files.

Mitigation: Review the target and effect, then obtain explicit user confirmation before each write, deletion, or sharing action.

Risk: Persistent triggers and destinations can forward data automatically after setup.

Mitigation: Disclose the destination and payload, require separate approval, and avoid forwarding OneDrive-derived data in event payloads.

## Reference(s):

- [Microsoft OneDrive skill on ClawHub](https://clawhub.ai/byungkyu/skills/one-drive)
- [Maton](https://maton.ai)
- [Microsoft Graph API reference](https://learn.microsoft.com/en-us/graph/api/overview)
- [OneDrive developer documentation](https://learn.microsoft.com/en-us/onedrive/developer/)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Guidance]

**Output Format:** [Markdown with CLI commands and occasional JSON or code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operations require an authorized OneDrive connection; write and sharing actions require user confirmation.]

## Skill Version(s):

1.2.5 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
