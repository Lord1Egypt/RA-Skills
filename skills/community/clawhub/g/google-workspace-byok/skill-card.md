## Description:

Google Workspace BYOK connects agents to Google Calendar and Gmail through a user's own Google Cloud OAuth client for calendar, email, attachment, and account-management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyesh](https://clawhub.ai/user/kyesh)

### License/Terms of Use:

ISC

## Use Case:

Users and developers use this skill to let an agent inspect Gmail and Google Calendar data, search messages, read events, check free/busy time, manage connected accounts, and download email attachments using user-provided Google Cloud OAuth credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Google OAuth credentials and tokens for Gmail and Calendar access.

Mitigation: Keep ~/.openclaw/google-workspace-byok owner-only, avoid shared machines, and revoke the Google OAuth grant when access is no longer needed.

Risk: Default authorization can request full Calendar read/write access along with Gmail read access.

Mitigation: Use the --readonly authorization mode unless Calendar writes are required for the intended workflow.

Risk: Downloaded email attachments may be written using filenames supplied by email content.

Mitigation: Download attachments only into a controlled directory, inspect filenames before use, and avoid processing unexpected attachments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyesh/skills/google-workspace-byok)
- [Google Cloud Console](https://console.cloud.google.com)
- [Google Auth Platform Audience](https://console.cloud.google.com/auth/audience)
- [Google Auth Platform Clients](https://console.cloud.google.com/auth/clients)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON command output, and downloaded attachment files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Gmail message reads truncate long bodies to 5000 characters; attachment actions can write downloaded files to a user-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
