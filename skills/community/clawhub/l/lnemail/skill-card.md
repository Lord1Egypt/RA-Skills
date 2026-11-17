## Description:

Setup and use anonymous email accounts on LNemail.net using Bitcoin Lightning payments. Use when agents need email capabilities for 2FA, notifications, or communication without KYC or personal information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnemail](https://clawhub.ai/user/lnemail)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to create and operate LNemail.net email accounts for anonymous signup flows, 2FA code reception, notifications, and programmatic email communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LNemail.net receives and handles mailbox contents, including possible 2FA codes.

Mitigation: Use the skill only when third-party email handling is acceptable, and avoid this mailbox for high-value account recovery or regulated data.

Risk: The access token is sufficient for ongoing mailbox access if exposed.

Mitigation: Store the token in an OS secret store where possible; if a file is used, restrict the directory to 0700 and the credential file to 0600, and keep it out of source control, logs, sync tools, shared workspaces, and unencrypted backups.

## Reference(s):

- [LNemail](https://lnemail.net)
- [ClawHub skill page](https://clawhub.ai/lnemail/skills/lnemail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, curl, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for LNemail account creation, Lightning payment status checks, bearer-token use, inbox reads, and paid outbound email requests.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
