## Description:

Feishu integration for sending messages, creating and managing chat groups, listing accessible chats, and automating Feishu workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukaizj](https://clawhub.ai/user/lukaizj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow operators use this skill to let an agent send Feishu text or card messages, create group chats, list accessible chats, and retrieve Feishu tenant token status after configuring Feishu app credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured Feishu app can send messages and create or list chats.

Mitigation: Grant the narrowest Feishu permissions needed for the intended workflow and restrict the app to approved chats.

Risk: The token helper exposes part of a tenant access token.

Mitigation: Remove or disable the feishu_get_token capability before production use and avoid logging or sharing token output.

Risk: Messages sent through the skill may contain sensitive content.

Mitigation: Avoid sending secrets or regulated data through the tool unless the Feishu workspace and workflow are approved for that data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lukaizj/skills/lukaizj-feishu)
- [ClawHub Publisher Profile](https://clawhub.ai/user/lukaizj)
- [Project Homepage](https://github.com/lukaizj/feishu-integration-skill)
- [Feishu Developer Console](https://open.feishu.cn/)
- [Feishu Open API](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON-like tool result objects and Feishu text or interactive card messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET; optionally uses FEISHU_VERIFY_TOKEN for callbacks.]

## Skill Version(s):

0.1.0 (source: server release metadata and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
