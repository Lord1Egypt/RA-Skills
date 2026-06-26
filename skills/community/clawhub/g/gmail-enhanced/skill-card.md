## Description: <br>
Enhanced Gmail integration with advanced features including label management, attachment handling, advanced search, email parsing, and automated email processing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users can use this skill to connect an agent to Gmail for searching messages, managing labels, downloading attachments, parsing email content, and sending or auto-replying to email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email and modify mailbox state through broad Gmail scopes. <br>
Mitigation: Grant access only to accounts where this automation is acceptable, review auto-reply and bulk-processing rules before running them, and avoid using broad queries for destructive mailbox changes. <br>
Risk: OAuth token files provide continuing access to the mailbox if exposed. <br>
Mitigation: Store credentials and token files in protected locations, restrict filesystem access, and revoke or rotate tokens if they may have been exposed. <br>
Risk: Downloaded attachments may be unsafe or may overwrite files with matching names in the download directory. <br>
Mitigation: Treat downloaded attachments as untrusted, use a contained download directory, scan files before opening them, and review filename handling before unattended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason-aka-chen/gmail-enhanced) <br>
- [Gmail API documentation](https://developers.google.com/gmail/api) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>
- [Gmail API Python quickstart](https://developers.google.com/gmail/api/quickstart/python) <br>


## Skill Output: <br>
**Output Type(s):** [Code, API Calls, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Python module usage, Gmail API calls, downloaded attachment files, and structured text or JSON-like dictionaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google OAuth credentials and Gmail API scopes for read, send, labels, and modify access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
