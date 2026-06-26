## Description: <br>
Read and send email via IMAP/SMTP using local Node scripts for inbox checks, message fetch/search, attachment handling, and approved outbound email, with an optional watcher that can forward alerts via OpenClaw CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xvespertine](https://clawhub.ai/user/0xvespertine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill with a configured mailbox to check, search, fetch, and manage email, parse or download selected attachments, and prepare or send approved outbound messages. The optional watcher supports inbox polling and alert forwarding when the operator accepts the additional trust boundary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox credentials and message contents may be exposed if the credential file or agent responses are mishandled. <br>
Mitigation: Use a dedicated mailbox or app password, keep the credential file private, and avoid echoing secrets in agent responses or logs. <br>
Risk: The optional watcher can run OpenClaw over mailbox content and forward summaries to another channel. <br>
Mitigation: Enable the watcher only after reviewing the configured OpenClaw binary, destination channel, recipient, and automatic forwarding behavior. <br>
Risk: Outbound email commands can send real messages, including reply-all messages. <br>
Mitigation: Keep the preview-first workflow, require explicit approval before sending, and review recipients before broad reply-all use. <br>
Risk: Attachment send and download operations read or write local files. <br>
Mitigation: Keep ALLOWED_READ_DIRS and ALLOWED_WRITE_DIRS narrow and review attachment paths before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xvespertine/imap-smtp-mail) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured IMAP/SMTP credentials; outbound sending is preview-first and requires explicit approval.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
