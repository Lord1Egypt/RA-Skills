## Description: <br>
Local Gmail IMAP/SMTP access using a Google App Password for searching, reading, and sending Gmail without routing mail through Maton or a third-party proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alanwen168](https://clawhub.ai/user/alanwen168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to perform local Gmail list, search, read, and user-approved send operations from an agent environment. It is intended for direct Gmail IMAP/SMTP workflows where credentials remain on the local host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a user's Gmail mailbox through a Google App Password. <br>
Mitigation: Install only when that mailbox access is acceptable, keep the password in a private 0600 local file, and revoke or rotate the app password when access is no longer needed. <br>
Risk: Email could be sent to unintended recipients or with unintended content. <br>
Mitigation: Review recipients, subject, and body before sending; the helper requires explicit approval and the --confirm-send flag for send operations. <br>


## Reference(s): <br>
- [Gmail Local Skill](https://clawhub.ai/alanwen168/gmail-local) <br>
- [Publisher profile](https://clawhub.ai/user/alanwen168) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GMAIL_ADDRESS and GMAIL_APP_PASSWORD_FILE; send operations require explicit approval and --confirm-send.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
