## Description:

Use when configuring OpenClaw chat channels to send an immediate acknowledgement before the main reply starts. Supports Feishu and DingTalk, includes bilingual Chinese-English guidance, and requires the acknowledgement language to follow the active conversation language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sallyxie2026](https://clawhub.ai/user/sallyxie2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bot operators use this skill to configure OpenClaw Feishu and DingTalk channels so users receive a short acknowledgement before the full agent response. The skill helps standardize responsive bilingual acknowledgement behavior while keeping normal reply routing intact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An extra immediate acknowledgement before each full response may be unwanted or inconsistent with the norms of a Feishu or DingTalk workspace.

Mitigation: Confirm with bot owners that the acknowledgement behavior is desired and appropriate for the target channel before installing.

Risk: Users may misunderstand a short acknowledgement as task completion if the wording is too final.

Mitigation: Use acknowledgement text that clearly means the bot received the message and is thinking, and keep the full response on the normal reply pipeline.

## Reference(s):

- [OpenClaw Immediate Ack on ClawHub](https://clawhub.ai/sallyxie2026/skills/openclaw-immediate-ack)

## Skill Output:

**Output Type(s):** [guidance, configuration, text]

**Output Format:** [Markdown guidance with acknowledgement text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese-English acknowledgement pools for Feishu and DingTalk channel behavior.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata, released 2026-03-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
