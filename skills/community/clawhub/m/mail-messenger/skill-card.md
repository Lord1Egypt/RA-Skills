## Description:

Helps agents send email over SMTP, prepare IMAP retrieval workflows, and create webhook notifications for WeCom, Feishu, and DingTalk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send reports, generated files, and task notifications through email or messaging webhooks. It also provides mail-provider setup guidance and local outcome tracking to improve repeated mail workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound email and webhook actions can send sensitive content to unintended recipients or URLs.

Mitigation: Confirm recipients, message content, attachments, and webhook URLs before sending; use a test send before production delivery.

Risk: SMTP and IMAP workflows require mail credentials.

Mitigation: Use app-specific credentials through environment variables or a secret manager, avoid passing secrets on shared command lines, and never commit credentials.

Risk: The learner utility can persist local usage history, preferences, errors, and notes.

Mitigation: Review or disable learned_patterns.json persistence when notes could contain personal, confidential, or regulated information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/mail-messenger)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate outbound SMTP, IMAP, or webhook workflows; local learning history can be persisted to learned_patterns.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
