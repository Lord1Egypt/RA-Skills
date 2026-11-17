## Description:

Automate Microsoft 365 mailbox tasks via Microsoft Graph: read, search, draft, and send emails for Business and Consumer accounts with device-code authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tradmangh](https://clawhub.ai/user/tradmangh)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers use this skill to automate mailbox workflows such as listing unread mail, searching messages, reading message previews, creating drafts, and sending prepared drafts through Microsoft Graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth token caches are stored locally without explicit file-permission hardening.

Mitigation: Use the skill only on a trusted single-user machine unless token-cache permissions are hardened before use.

Risk: Broad Microsoft Graph scopes or offline access can increase mailbox exposure if credentials or token caches are compromised.

Mitigation: Request the narrowest Microsoft Graph scopes possible and avoid offline_access unless the workflow requires it.

Risk: Draft capability can create mailbox drafts without the stated per-action confirmation check in this version.

Mitigation: Review policy settings before enabling draft capability and inspect generated drafts before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tradmangh/skills/m365-mailbox)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print mailbox metadata, message previews, draft identifiers, setup prompts, and Microsoft Graph error messages.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
