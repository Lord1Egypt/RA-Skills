## Description:

Google Workspace CLI for Gmail, Calendar, Chat, Classroom, Drive, Docs, Slides, Sheets, Forms, Apps Script, Contacts, Tasks, People, Admin, Groups, and Keep.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iiroak](https://clawhub.ai/user/iiroak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to guide agents in running gog CLI commands for Google Workspace administration, content access, messaging, calendar operations, file handling, and automation. It emphasizes command discovery, JSON output, and explicit confirmation for sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports broad Google Workspace access across email, Drive, admin, credentials, webhooks, and tracking.

Mitigation: Install only when the gog CLI source is trusted, use the narrowest OAuth scopes, and apply command allowlists where possible.

Risk: Sensitive actions such as sending mail, creating events, deleting resources, sharing files, forwarding mail, delegation, tracking, and admin changes can affect users or data.

Mitigation: Require explicit approval for these operations, prefer dry runs when available, and avoid --force or --no-input for sensitive actions.

Risk: The documented Homebrew installation is a third-party install path and is not pinned in the evidence.

Mitigation: Review the package source and installed gog binary before granting Google Workspace credentials or service account access.

Risk: Webhook and email tracking commands can send data to external destinations.

Mitigation: Review hook URLs, tracking worker URLs, shared tokens, and OIDC settings before enabling watch or tracking workflows.

## Reference(s):

- [GoG CLI homepage](https://gogcli.sh)
- [ClawHub release page](https://clawhub.ai/iiroak/skills/gog-complete)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON or TSV output guidance for gog command results.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
