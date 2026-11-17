## Description:

Manage Microsoft 365 work/school account services including Exchange, OneDrive for Business, SharePoint, calendar, and organizational user search through the m365 CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrhah](https://clawhub.ai/user/mrhah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage Microsoft 365 work/school mail, calendar, OneDrive for Business, SharePoint, and organization user search through m365 CLI commands and JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Corporate mail and business files may be exposed through broad Microsoft 365 access or unsafe command choices.

Mitigation: Review before installation on sensitive accounts, use only work/school accounts, and require explicit confirmation before sending, deleting, or sharing content.

Risk: Bypassing trusted-sender filtering with --force can expose agents to untrusted email content.

Mitigation: Avoid --force unless the sender and message have been confirmed, and summarize email content instead of echoing full bodies by default.

Risk: Anonymous sharing can make OneDrive or SharePoint files accessible to anyone with the link.

Mitigation: Prefer named-user or organization-scoped sharing over anonymous links.

Risk: A globally installed m365-cli package could execute unexpected code if the package source is not verified.

Mitigation: Pin or verify the m365-cli package before global installation.

## Reference(s):

- [m365-cli command reference](references/commands.md)
- [ClawHub skill page](https://clawhub.ai/mrhah/skills/m365cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to prefer --json output from m365 commands and to confirm sensitive mail, file, calendar, and sharing actions.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
