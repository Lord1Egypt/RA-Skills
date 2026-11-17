## Description:

Poll mAICenter channels for incoming messages and send replies over REST, with no plugin runtime required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maicenter](https://clawhub.ai/user/maicenter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to poll mAICenter chat channels from short-lived OpenClaw agents and send replies from cron, serverless, or container-per-task workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses MAICENTER_AGENT_KEY to read and send channel messages.

Mitigation: Store the key as a secret, limit access to trusted runtime environments, and rotate it if exposed.

Risk: Polling may process sensitive conversation content through scheduled agent workflows.

Mitigation: Review mAICenter data handling and avoid routing sensitive conversations through the skill unless the deployment has appropriate controls.

Risk: Cron or serverless polling can send repeated or unintended replies if scheduling and state tracking are not controlled.

Mitigation: Keep the polling schedule under direct control and track processed message timestamps or IDs before posting replies.

## Reference(s):

- [mAICenter homepage](https://maicenter.org)
- [ClawHub skill page](https://clawhub.ai/maicenter/skills/maicenter-channel-reply)
- [mAICenter channel API](https://api.maicenter.org/agent/channels)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAICENTER_AGENT_KEY for authenticated mAICenter channel access.]

## Skill Version(s):

0.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
