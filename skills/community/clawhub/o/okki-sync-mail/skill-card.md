## Description: <br>
Okki Sync Mail helps agents read and manage IMAP mailboxes, send SMTP email, generate or review replies, archive messages, and sync inbound and outbound email activity to OKKI CRM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and operations teams use this skill to triage mailbox activity, prepare or send customer email, and sync customer communication to OKKI CRM follow-up records. Operators configure mailbox, CRM, local knowledge, and optional review integrations before enabling live mailbox or outbound email workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access live mailbox data and archive email content locally. <br>
Mitigation: Use a dedicated mailbox, restrict configured read and write directories, and review archived content handling before production use. <br>
Risk: The skill can send or schedule customer-facing email through SMTP. <br>
Mitigation: Require dry-run previews and explicit human confirmation before any live send, reply, draft send, or scheduled send. <br>
Risk: Email-derived content may be sent to third-party AI or Discord review services when those paths are configured. <br>
Mitigation: Disable OpenRouter and Discord integrations unless approved, and avoid sending sensitive customer or business data to unapproved external services. <br>
Risk: The skill can write follow-up records into OKKI CRM. <br>
Mitigation: Test against a non-production OKKI workspace first and verify customer matching before enabling automatic CRM writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjboy007/okki-sync-mail) <br>
- [Publisher profile](https://clawhub.ai/user/cjboy007) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can initiate mailbox reads, CRM writes, local archiving, third-party review calls, and outbound email actions when configured and approved.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
