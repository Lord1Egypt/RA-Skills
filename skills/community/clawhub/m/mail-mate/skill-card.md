## Description: <br>
Mail Mate connects to IMAP mailboxes, filters messages by provider, time window, subject, and body keywords, extracts structured fields with regular expressions, and can optionally push matching results to DingTalk, Feishu, or Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tankeito](https://clawhub.ai/user/tankeito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to retrieve recent or time-bounded IMAP email, normalize and filter message content, extract structured fields, and route concise results into downstream agent workflows or trusted notification channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox credentials and app passwords are sensitive and are required for normal IMAP access. <br>
Mitigation: Use a dedicated or least-privilege mailbox where possible, keep credentials out of shared logs, and remove generated .env files when scheduled processing is no longer needed. <br>
Risk: Filtered email previews and extracted fields may contain private or business-sensitive content, especially when pushed to chat platforms. <br>
Mitigation: Keep filters narrow, reduce preview_length for sensitive mail, and enable DingTalk, Feishu, or Telegram delivery only to trusted destinations. <br>
Risk: Scheduled cron execution can continue reading mail after the immediate task is complete. <br>
Mitigation: Review the installed crontab entry and remove it when recurring processing is no longer intended. <br>


## Reference(s): <br>
- [Mail Mate on ClawHub](https://clawhub.ai/tankeito/mail-mate) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration] <br>
**Output Format:** [JSON result objects, optional Markdown push messages, and shell/configuration guidance for scheduled execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns mailbox server, time window, filter description, count, matching email summaries, extracted_data fields, previews, and optional push status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
