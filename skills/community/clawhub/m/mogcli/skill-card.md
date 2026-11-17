## Description:

Microsoft Ops Gadget - CLI for Microsoft 365 (Mail, Calendar, Drive, Contacts, Tasks, Word, PowerPoint, Excel, OneNote).

This skill is ready for commercial/non-commercial use.

## Publisher:

[visionik](https://clawhub.ai/user/visionik)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use Mog to operate Microsoft 365 resources from a CLI, including mail, calendar, OneDrive, contacts, tasks, Word, PowerPoint, Excel, and OneNote workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can modify or delete Microsoft 365 account data.

Mitigation: Review proposed delete, send, update, upload, and write commands before allowing an agent to execute them.

Risk: The CLI requests broad delegated Microsoft 365 access, including refresh-token access.

Mitigation: Install only for accounts where that access level is acceptable and prefer a pinned source version.

Risk: Token storage behavior is flagged as misleading, and ~/.config/mog/tokens.json should be treated as sensitive plaintext.

Mitigation: Protect the config directory, avoid exposing token files to agents or logs, and rotate credentials if token files are disclosed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/visionik/skills/mogcli)
- [Go package documentation](https://pkg.go.dev/github.com/visionik/mogcli)
- [Azure Portal app registrations](https://portal.azure.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Microsoft 365 read, send, update, delete, upload, download, and authentication commands for review before execution.]

## Skill Version(s):

0.3.1 (source: server release metadata and changelog, released 2026-01-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
