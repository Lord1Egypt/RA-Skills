## Description:

Bulletproof LinkedIn inbox monitoring with progressive autonomy. Monitors messages hourly, drafts replies in your voice, and alerts you to new conversations. Supports 4 autonomy levels from monitor-only to full autonomous.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dylanbaker24](https://clawhub.ai/user/dylanbaker24)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to monitor LinkedIn inbox activity, receive alerts for new conversations, and prepare replies for review or limited automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on persistent access to a logged-in LinkedIn account.

Mitigation: Use a dedicated browser profile, avoid plaintext storage of session cookies, and disable cron or remove local state when monitoring is no longer needed.

Risk: Private message previews and drafted replies may be sent to an external alert channel.

Mitigation: Confirm the configured alert destination and its membership before enabling monitoring.

Risk: Higher autonomy levels can send messages as the user.

Mitigation: Keep the skill at monitor-only or draft-approval mode unless the user explicitly accepts autonomous sending.

Risk: Untrusted LinkedIn message content can influence drafted replies.

Mitigation: Review drafted replies before sending and escalate sensitive, legal, angry, refund, or ambiguous conversations to a human.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dylanbaker24/skills/linkedin-monitor)
- [Clawdbot](https://github.com/clawdbot/clawdbot)
- [LinkedIn Messaging](https://www.linkedin.com/messaging/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include alert text, drafted replies, setup guidance, health status, and local state/configuration updates.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
