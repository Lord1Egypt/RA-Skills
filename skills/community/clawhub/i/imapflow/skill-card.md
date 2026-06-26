## Description: <br>
Modern Node.js IMAP client library guidance for email integration, covering authentication, mailbox locking, streaming fetches, async iterators, reconnection strategies, proxy support, and provider-specific configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to write Node.js IMAP integrations with ImapFlow, including connecting to providers, fetching and searching messages, managing mailboxes, handling IDLE notifications, and using provider-specific authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated code may expose mailbox credentials or OAuth tokens if they are hard-coded, logged, or stored insecurely. <br>
Mitigation: Use app-specific passwords or scoped OAuth tokens, keep secrets outside source code, and avoid logging authentication values. <br>
Risk: Generated mailbox operations can move, delete, expunge, flag, append, or otherwise change email data. <br>
Mitigation: Require explicit user confirmation before write or destructive actions and preview affected message ranges before execution. <br>
Risk: Fetching broad message ranges or full message sources can disclose more email content than needed. <br>
Mitigation: Fetch the smallest needed message range and fields, and prefer envelope, headers, or targeted body parts over full sources when possible. <br>


## Reference(s): <br>
- [ImapFlow API Reference](references/api_reference.md) <br>
- [IMAP Connection Configurations](references/connection.md) <br>
- [IMAP Search Key Reference](references/searching.md) <br>
- [Proton Mail Bridge](https://proton.me/mail/bridge) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; generated code may access or change mailbox data when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
