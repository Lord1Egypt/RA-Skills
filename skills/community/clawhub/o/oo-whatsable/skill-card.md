## Description:

WhatsAble (whatsable.app). Use this skill for ANY WhatsAble request — reading, creating, and updating data. Whenever a task involves WhatsAble, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users use the skill to send a WhatsApp text message through their connected WhatsAble account, optionally with an attachment URL. Before sending, the agent checks the connector's live input schema and confirms the exact payload with the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded CLI code and may install an agent skill without a separate approval step; the installer's precise local effects are unverified.

Mitigation: Before setup, review and verify the chosen CLI release and its automatic agent-skill installation behavior.

Risk: Message contents and attachment URLs pass through OOMOL.

Mitigation: Confirm the recipient and exact message or attachment URL before each send.

## Reference(s):

- [WhatsAble API: Send a WhatsApp message](https://docs.whatsable.app/api-reference/whatsable/messages/send-a-whatsapp-message)
- [WhatsAble](https://whatsable.app)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [WhatsAble ClawHub release](https://clawhub.ai/oomol/skills/oo-whatsable)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Connector action requests and JSON responses; WhatsApp text messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A message may include an attachment URL; sending changes WhatsAble state and requires confirmation of the exact payload.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
