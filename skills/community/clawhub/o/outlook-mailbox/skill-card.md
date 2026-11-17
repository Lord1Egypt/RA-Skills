## Description:

Guides administrators in granting app-only Microsoft Graph access to named Exchange Online mailboxes, verifying the scope, and restricting mail operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Microsoft 365 administrators and developers use this skill to limit an agent's Outlook mailbox access to an approved list, test that other mailboxes remain inaccessible, and guide restricted reads and reply drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Additional mail permissions could expose mailboxes outside the approved scope.

Mitigation: Remove unscoped Entra mail grants and verify both an approved mailbox and an excluded mailbox before use.

Risk: Mailbox content may contain sensitive personal information.

Mitigation: Obtain data-controller approval for purpose, mailbox list, fields, retention, and owner notice; keep mail content out of logs and persistent storage.

Risk: Broad mail rights could permit unwanted message changes or credential exposure.

Mitigation: Keep Graph credentials outside the agent, require the runtime call allowlist, and limit writes to approved reply drafts.

## Reference(s):

- [Microsoft Learn: Role Based Access Control for Applications in Exchange Online](https://learn.microsoft.com/en-us/exchange/permissions-exo/application-rbac)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Text]

**Output Format:** [Markdown guidance with PowerShell and shell examples, JSON policy examples, and a plain-text scope record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scope record documents approved mailboxes and positive and negative access checks.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
