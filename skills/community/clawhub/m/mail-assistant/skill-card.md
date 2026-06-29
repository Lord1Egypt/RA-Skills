## Description: <br>
Unified email management assistant supporting Outlook/M365 via Microsoft Graph OAuth2, 163, and QQ mailboxes for reading, sending, searching, summarizing, auto-reply rules, scheduled sync, attachments, CC/BCC, and read/unread status management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanfan-2011](https://clawhub.ai/user/fanfan-2011) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
End users and agents use this skill to configure local mailbox access and manage email workflows across Outlook/Microsoft 365, 163, and QQ accounts. It supports inbox review, search, message drafting and sending, auto-reply rule management, scheduled synchronization, and attachment handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests read, write, and send access to configured mailboxes. <br>
Mitigation: Install only for accounts where that access is acceptable, review requested permissions during OAuth, and revoke access in the provider account portal when no longer needed. <br>
Risk: Mailbox credentials and tokens are stored locally, and keyring support may depend on the user's environment. <br>
Mitigation: Install keyring support where available, keep the email assistant data directory out of version control and backups that are broadly shared, and rotate provider authorization codes or tokens if exposure is suspected. <br>
Risk: Auto-reply rules can create unwanted replies, reply loops, spam amplification, or accidental disclosure through attachments. <br>
Mitigation: Preview rules with dry-run, prefer narrow sender or keyword conditions over catch-all rules, review attachments before enabling replies, and periodically remove stale rules. <br>
Risk: The bundled shared Azure application may not match every organization's security requirements. <br>
Mitigation: Use an organization-controlled Azure app registration when stricter tenant control, auditing, or application ownership is required. <br>


## Reference(s): <br>
- [Microsoft Graph API Reference](artifact/references/microsoft_graph.md) <br>
- [Email Protocol Configuration Reference](artifact/references/email_protocols.md) <br>
- [Auto-Reply Rules Reference](artifact/references/auto_reply_rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fanfan-2011/mail-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include local OAuth setup, mailbox synchronization, and user-confirmed write operations.] <br>

## Skill Version(s): <br>
1.8.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
