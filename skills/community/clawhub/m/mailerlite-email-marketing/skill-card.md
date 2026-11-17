## Description:

Manage MailerLite email marketing campaigns, automations, subscribers, and e-commerce stores. Create campaigns, manage groups and segments, handle subscribers, and track e-commerce activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate MailerLite marketing workflows from an agent, including campaign, automation, subscriber, group, segment, webhook, and e-commerce account tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform sensitive MailerLite account actions, including subscriber deletion, campaign sending, automation changes, and e-commerce updates.

Mitigation: Review connected account permissions, preview write actions, and confirm every write or destructive action before execution.

Risk: The skill depends on ClawLink for hosted connection flows and credential handling.

Mitigation: Install only when ClawLink is trusted, keep the MailerLite connection scoped to the intended account, and revoke the connection when it is no longer needed.

## Reference(s):

- [MailerLite API Documentation](https://developers.mailerlite.com/)
- [MailerLite Integrations](https://www.mailerlite.com/integrations)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/mailerlite-email-marketing)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions]

**Output Format:** [Markdown with inline bash commands and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected MailerLite account through ClawLink; write and destructive actions require explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
