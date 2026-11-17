## Description:

Google Workspace CLI for Gmail, Calendar, and Drive using official Google APIs for direct access without third-party proxies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jfab68](https://clawhub.ai/user/jfab68)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure and run a local Google Workspace CLI for Gmail search, label, draft, and send tasks; Calendar listing and event creation; and Drive file search and metadata lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests sensitive Google account access for Gmail modification, Calendar access, and Drive read-only access.

Mitigation: Use a least-privilege Google account or test Workspace project, verify the OAuth client before authorization, and revoke the OAuth grant when access is no longer needed.

Risk: OAuth credentials and tokens are stored locally under ~/.config/praxis-gws/.

Mitigation: Restrict access to the local configuration directory and revoke the OAuth grant if token exposure is suspected.

Risk: The setup guidance may require bypassing Google's unverified app warning for a user-created OAuth client.

Mitigation: Proceed only after confirming the Google Cloud project and OAuth client are the intended ones.

Risk: The documented global googleapis dependency install may resolve an unpinned package version.

Mitigation: Prefer a pinned local dependency install for repeatable review and execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jfab68/skills/praxis-gws)
- [Google Cloud Console](https://console.cloud.google.com)
- [Gmail modify OAuth scope](https://www.googleapis.com/auth/gmail.modify)
- [Google Calendar OAuth scope](https://www.googleapis.com/auth/calendar)
- [Google Drive read-only OAuth scope](https://www.googleapis.com/auth/drive.readonly)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI itself emits plain text status messages and JSON-formatted Google API responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
