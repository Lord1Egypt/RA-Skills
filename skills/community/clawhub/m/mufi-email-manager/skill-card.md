## Description:

Mufi Email Manager helps agents manage Gmail, Naver, Daum, and Kakao mail over IMAP/SMTP with unread-mail checks, keyword filtering, mailbox summaries, and template-based replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to configure a Korean email management helper, review unread messages, identify important mail, summarize mailbox activity, and prepare template replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires email account credentials and mailbox access.

Mitigation: Use app-specific passwords where available, configure only the accounts needed, and avoid storing reusable passwords outside protected environment configuration.

Risk: Reply and scheduled examples can affect real recipients.

Mitigation: Review generated replies and cron jobs before use, and avoid unattended sending until operational controls are in place.

Risk: The documentation overstates some available commands and features.

Mitigation: Confirm that referenced scripts exist and run successfully before relying on documented digest, send, search, or notification workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/mufi-email-manager)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured email account credentials and network access to IMAP/SMTP servers.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
