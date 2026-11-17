## Description:

Set up Gmail API access via the gog CLI with a manual OAuth flow for headless servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kai-jar](https://clawhub.ai/user/kai-jar)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure Gmail API OAuth credentials, generate authorization URLs, exchange authorization codes, import refresh tokens into gog, and troubleshoot Gmail authentication on headless servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default Gmail scope can grant broad mailbox access.

Mitigation: Use the least Gmail scope that fits the task, such as read-only or send-only access when modification access is not needed.

Risk: OAuth secrets may persist in the environment, keyring configuration, or a temporary token import file.

Mitigation: Prefer a secure keyring or one-session secret, avoid storing GOG_KEYRING_PASSWORD in shell startup files, and confirm temporary token files are removed after import.

Risk: The helper relies on the external gog CLI for handling OAuth credentials.

Mitigation: Verify the gog CLI source and version before trusting it with OAuth credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kai-jar/skills/gmail-oauth)
- [Google Cloud Console](https://console.cloud.google.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands and an optional bash helper for generating Gmail OAuth URLs and exchanging authorization codes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
