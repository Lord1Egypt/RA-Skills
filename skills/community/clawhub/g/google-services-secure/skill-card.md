## Description:

Secure Google Workspace integration (Gmail, Drive, Calendar, Sheets, Docs, Contacts, etc.) with enterprise-grade security.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nelmaz](https://clawhub.ai/user/nelmaz)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation builders use this skill to configure OAuth-based access to Google Workspace services, validate setup, and generate shell/API workflows for Gmail, Drive, Calendar, Sheets, Docs, and Contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports that the implementation does not match its strong security claims and stores OAuth tokens in a predictable local file.

Mitigation: Review token storage, OAuth request binding, permission enforcement, confirmations, validation, and rate limiting before using sensitive Google Workspace accounts.

Risk: The skill can access sensitive mail, files, calendars, documents, spreadsheets, and contacts when credentials and scopes permit it.

Mitigation: Evaluate with low-scope test credentials first, keep permission mode read-only unless writes are required, and use the minimum OAuth scopes needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nelmaz/skills/google-services-secure)
- [Security Guide](references/security.md)
- [Gmail API Reference](https://developers.google.com/gmail/api/reference/rest/)
- [Google Drive API Reference](https://developers.google.com/drive/api/reference/rest/v3/)
- [Google Calendar API Reference](https://developers.google.com/calendar/api/v3/reference/)
- [Google Sheets API Reference](https://developers.google.com/sheets/api/reference/rest/)
- [Google People API Reference](https://developers.google.com/people/api/rest/v1/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash, curl, JSON, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google API and OAuth client environment variables.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, artifact metadata, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
