## Description: <br>
Read, search, send, trash, move, and label Gmail via IMAP using Gmail address and Google App Password environment variables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottgl9](https://clawhub.ai/user/scottgl9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent access Gmail mailboxes for inbox review, search, message reading, sending, moving, labeling, and trashing messages through IMAP and SMTP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports that a UID-handling mismatch could cause the agent to read, move, or trash the wrong email. <br>
Mitigation: Install only for trusted agents, manually verify UID behavior before destructive actions, and review read, move, and trash operations carefully. <br>
Risk: The skill requires Gmail credentials that can access mailbox contents and send or modify email. <br>
Mitigation: Use a dedicated, revocable Google App Password and avoid sharing the credential with untrusted agents or workspaces. <br>


## Reference(s): <br>
- [Gmail IMAP Reference](references/gmail-imap-reference.md) <br>
- [ClawHub Gmail IMAP Skill](https://clawhub.ai/skills/gmail-imap) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May display email metadata, message bodies, send status, and move/trash confirmations; requires Gmail credential environment variables.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
