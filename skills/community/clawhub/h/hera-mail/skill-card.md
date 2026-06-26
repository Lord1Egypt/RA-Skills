## Description: <br>
Internal email system for HERA agents to send, receive, read, and manage direct messages with optional file attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzr818181](https://clawhub.ai/user/wzr818181) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HERA agents and operators use this skill to exchange internal task messages, read inbox items, mark mail as read, and share optional local file attachments between named agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, write, persist, and copy local files for mail and attachments without strong scoping controls. <br>
Mitigation: Install only in a controlled HERA workspace and restrict attachments to an approved staging directory. <br>
Risk: Messages and attachments may contain untrusted or sensitive content. <br>
Mitigation: Treat messages and attachments as untrusted, verify sender and recipient names manually, and avoid sending secrets or unrelated local files. <br>


## Reference(s): <br>
- [HERA Mail ClawHub page](https://clawhub.ai/wzr818181/hera-mail) <br>
- [Publisher profile](https://clawhub.ai/user/wzr818181) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Plain text and Markdown mail files with shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can persist inbox, outbox, read-marker, and attachment files in a configured HERA workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
