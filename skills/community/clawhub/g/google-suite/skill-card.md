## Description:

Provides unified access to Gmail, Google Calendar, and Google Drive APIs for managing emails, calendar events, and files with OAuth2 authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cenralsolution](https://clawhub.ai/user/cenralsolution)

### License/Terms of Use:


## Use Case:

Developers and agent operators can use this skill to connect an agent to Google Workspace services for email, calendar, and Drive workflows after OAuth setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad OAuth scopes allow read, write, and delete access across Gmail, Calendar, Drive, and local files.

Mitigation: Use a dedicated Google account or least-privilege OAuth app where possible, review destructive actions before invoking them, and revoke or delete google_suite_tokens.json when the environment is no longer trusted.

Risk: Drive upload and download actions can move sensitive local files or write to caller-provided destination paths.

Mitigation: Restrict local paths manually and avoid uploading sensitive files unless the runtime, Google account, and destination path are trusted.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/cenralsolution/skills/google-suite)
- [Google API Python Client](https://github.com/googleapis/google-api-python-client)
- [Gmail API Docs](https://developers.google.com/gmail/api)
- [Calendar API Docs](https://developers.google.com/calendar/api)
- [Drive API Docs](https://developers.google.com/drive/api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files, Configuration instructions]

**Output Format:** [Structured Python return values, status objects, downloaded files, and OAuth setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local OAuth token files and write downloaded Drive content to caller-provided paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
