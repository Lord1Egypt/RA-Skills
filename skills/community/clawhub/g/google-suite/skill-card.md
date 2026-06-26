## Description: <br>
Provides unified access to Gmail, Google Calendar, and Google Drive APIs for managing emails, calendar events, and files with OAuth2 authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cenralsolution](https://clawhub.ai/user/Cenralsolution) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to manage Gmail messages, Google Calendar events, and Google Drive files from an agent workflow through OAuth2-authenticated Google APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad persistent Google account access can expose Gmail, Calendar, and Drive data beyond the immediate task. <br>
Mitigation: Use a low-risk or dedicated Google account where possible and grant only the access needed for the intended workflow. <br>
Risk: Send, delete, update, upload, and download actions can make high-impact changes without built-in safeguards. <br>
Mitigation: Require human confirmation before actions that send messages, modify events, delete records, upload files, or download private data. <br>
Risk: The OAuth token file can provide ongoing access if copied or exposed. <br>
Mitigation: Keep google_suite_tokens.json private, remove it when no longer needed, and revoke the Google OAuth grant after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Cenralsolution/google-suite) <br>
- [Google API Python Client](https://github.com/googleapis/google-api-python-client) <br>
- [Gmail API Docs](https://developers.google.com/gmail/api) <br>
- [Google Calendar API Docs](https://developers.google.com/calendar/api) <br>
- [Google Drive API Docs](https://developers.google.com/drive/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, API results] <br>
**Output Format:** [Structured Python dictionaries and lists containing status values, object IDs, email snippets, calendar event data, Drive file metadata, and local file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can create external side effects in the connected Google account, including sending or deleting email, creating or deleting calendar events, uploading or deleting Drive files, and downloading Drive files to local paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md, config.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
