## Description:

A daily lyrics blessing skill that fetches Hetu song lyrics from Baidu Baike and sends a scheduled reminder message by email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trae1oung](https://clawhub.ai/user/trae1oung)

### License/Terms of Use:


## Use Case:

External users can use this skill to configure a daily email reminder that includes a Hetu lyric and blessing message. It is intended for scheduled personal messaging where the sender reviews and supplies their own email configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports real-looking SMTP credentials and fixed sender and recipient values.

Mitigation: Remove or rotate the exposed credential before use and configure sender, password, and recipient values through a secured local configuration.

Risk: The skill includes persistent cron setup for recurring email delivery.

Mitigation: Add the cron entry only after confirming the schedule, recipient, and removal procedure.

Risk: The setup installs browser automation globally and uses it to fetch lyric text from Baidu Baike.

Mitigation: Review the dependency installation path, prefer pinned or controlled installation where possible, and verify fetched content before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trae1oung/skills/hetu-lyrics-blessing)
- [Baidu Baike](https://baike.baidu.com)
- [Baidu Baike lyric source example](https://baike.baidu.com/item/%E5%80%BE%E5%B0%BD%E5%A4%A9%E4%B8%8B)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python configuration snippets; plain-text email content at runtime]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SMTP email delivery, scheduled cron execution, browser automation for lyric lookup, and local fallback lyric text when lookup fails.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
