## Description: <br>
Reads email from POP3 mailboxes in a read-only mode, returning mailbox counts, recent subjects, full messages, message-by-index results, and subject keyword search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyun2000](https://clawhub.ai/user/yuyun2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect mailbox contents through POP3 SSL without deleting or modifying messages. It is useful for checking recent mail, finding messages by subject keyword, or reading specific messages after the user provides mailbox credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox credentials can expose sensitive email contents to the agent and any process that can read the configured secret. <br>
Mitigation: Use a revocable app-specific password or authorization code, scope it to the mailbox account, and revoke it after the task is complete. <br>
Risk: Passing credentials on the command line or storing them in a plaintext .email_config file can leave secrets in shell history, process listings, or local files. <br>
Mitigation: Prefer environment variables or a managed secret store, avoid command-line passwords, set local config permissions to 600, and remove stored credentials after use. <br>
Risk: Email bodies, attachments, and verification codes are highly sensitive and may be surfaced in agent responses. <br>
Mitigation: Ask for explicit user consent before reading messages, limit reads to the smallest necessary range, and redact or summarize sensitive content when presenting results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyun2000/m5-email-reader) <br>
- [POP3 provider configuration reference](references/providers.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON from the Python script; natural-language summaries may be produced by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include email metadata, body text, attachment names and sizes; long bodies should be truncated by the agent when presenting to users.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
