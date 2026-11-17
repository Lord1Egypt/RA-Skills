## Description:

Connects an agent to a user's Google Drive and Sheets account through OAuth so it can create, read, update, format, and delete files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinhbuiii](https://clawhub.ai/user/thinhbuiii)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent can authorize access to their own Google account so the agent can manage Drive files and spreadsheet data. Developers or administrators can configure an OAuth app for individual or team use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The login flow can expose sensitive authorization codes in chat.

Mitigation: Use a protected login callback that keeps authorization codes out of chat.

Risk: The formatting command may bypass deletion safeguards.

Mitigation: Restrict formatting to formatting operations.

Risk: Drive file deletion permanently removes files.

Mitigation: Confirm the target before deletion, and revoke access through Google account permissions when finished.

Risk: The connection requests broad Drive access.

Mitigation: Use narrower file access where possible.

## Reference(s):

- [Google Drive API: Delete a file](https://developers.google.com/workspace/drive/api/reference/rest/v3/files/delete)
- [ClawHub release page](https://clawhub.ai/thinhbuiii/skills/google-sheets-connect)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Text, JSON]

**Output Format:** [Command-line instructions, OAuth URLs, and text or JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operations use the permissions of the Google account that authorized access.]

## Skill Version(s):

1.4.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
