## Description:

Set up an autonomous, customer-facing OpenClaw support agent inside an Intercom inbox across WhatsApp, Instagram, Facebook, Messenger, SMS, and email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[othreecodes](https://clawhub.ai/user/othreecodes)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams and developers use this skill to configure an OpenClaw Intercom channel that lets an agent answer customer conversations directly, process screenshots and voice notes, and hand off to humans cleanly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can send real customer-facing replies under a teammate identity.

Mitigation: Get support-workspace authorization before enabling it, start with one low-risk channel, configure a real human handoff target, and monitor early conversations.

Risk: Intercom app credentials and broad conversation permissions could increase impact if reused or over-scoped.

Mitigation: Use a dedicated Intercom app token with only the permissions needed for the rollout, and keep the token rotatable.

Risk: Poor workspace grounding can produce off-scope or incorrect customer replies, including mistakes about screenshots.

Mitigation: Add product-specific support rules to the agent workspace, instruct the agent not to identify which app a screenshot belongs to, and require it to ask rather than assert when uncertain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/othreecodes/skills/intercom-support-channel)
- [OpenClaw Intercom source and configuration reference](https://github.com/othreecodes/openclaw-intercom)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes rollout, authorization, token-scoping, channel-scoping, and human-handoff guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
