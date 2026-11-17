## Description:

Captures user ideas, wishes, complaints, and pain points during conversation, appends them to an inbox file without confirmation, and supports scheduled review summaries for Telegram and Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guytogay](https://clawhub.ai/user/guytogay)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use this skill to capture product ideas, feature requests, wishes, complaints, and pain points from everyday agent conversations for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill silently logs broad conversation content.

Mitigation: Use it only with an explicitly configured private inbox and avoid chats containing secrets, personal data, workplace-sensitive material, health or financial information, or third-party confidential content.

Risk: Captured content can be forwarded to external Telegram and Feishu destinations without sufficient user control.

Mitigation: Configure only private destinations and add opt-in capture, visible notifications, redaction, review-before-send, and deletion controls before using it in sensitive contexts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guytogay/skills/ken-idea-capture)
- [ClawHub Publisher Profile](https://clawhub.ai/user/guytogay)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown inbox entries and review summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Captured entries include timestamped original text and source channel when configured.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
