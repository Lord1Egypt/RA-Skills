## Description: <br>
Monitors an IMAP mailbox with IDLE and sends new-mail notifications to a configured Feishu user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apple133junjiang-a11y](https://clawhub.ai/user/apple133junjiang-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a long-lived mailbox listener that detects new mail without polling and forwards concise notifications to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email sender details, subjects, summaries, and possible body excerpts may be forwarded to Feishu. <br>
Mitigation: Use only with mailboxes where that sharing is approved, limit recipients, and reduce or disable body excerpts before using it with sensitive email. <br>
Risk: Local notification and log files may retain sensitive mail metadata or content. <br>
Mitigation: Protect the workspace files, reduce stored fields where possible, and define retention or cleanup for generated notification and log data. <br>
Risk: Mailbox and Feishu credentials are configured for the listener workflow. <br>
Mitigation: Use app-specific credentials with the least required access and keep real secrets out of shared skill files and logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/apple133junjiang-a11y/imap-idle-sender) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included listener can create local JSON notification records and log files when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
