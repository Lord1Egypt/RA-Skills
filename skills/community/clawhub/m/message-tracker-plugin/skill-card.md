## Description:

Sends formatted tracked messages to Feishu channels via webhook with automatic retry on failure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjl1004](https://clawhub.ai/user/wjl1004)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to send tracked message events or monitoring results to Feishu channels as structured webhook cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu webhook URLs and optional secrets are credentials that could allow unauthorized message posting if exposed.

Mitigation: Configure webhooks only for intended channels and keep webhook URLs and secrets out of public repositories.

Risk: Chinese-only instructions can increase operator misunderstanding for teams that do not read Chinese.

Mitigation: Confirm installers are comfortable with the instructions or provide a reviewed translation before use.

## Reference(s):

- [Message Tracker Plugin on ClawHub](https://clawhub.ai/wjl1004/skills/message-tracker-plugin)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript examples and configuration fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu webhook payload guidance, retry settings, and HMAC-SHA256 signing notes.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
