## Description:

Automates marketing workflows across Feishu, DingTalk, and WeCom by guiding agents through content creation, multi-channel distribution, campaign tracking, lead nurturing, and performance reporting with official CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, sales, and operations teams use this skill to coordinate approved campaign content, lead tracking, customer nurture, and reporting across Feishu, DingTalk, and WeCom. Agents use it to produce platform-specific workflow guidance and shell commands for normal marketing operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated marketing commands can contact the wrong chat, recipient, or customer segment.

Mitigation: Verify target chats, recipients, approval status, and customer segment selection before running any generated command.

Risk: Customer outreach or data syncing can violate consent, unsubscribe, frequency, or privacy requirements.

Mitigation: Confirm opt-in and unsubscribe state, apply frequency caps, and verify that customer data may legally be copied between platforms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/marketing-automation-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and platform workflow tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed for correct recipients, approvals, consent, opt-out status, and frequency limits before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
