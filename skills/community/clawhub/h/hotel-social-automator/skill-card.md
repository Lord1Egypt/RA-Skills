## Description: <br>
Generate, review, and publish social media content through MCP with AgentAuth and workspace token authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tourmind](https://clawhub.ai/user/tourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hotel marketing teams and their agents use this skill to generate, review, publish, and schedule social media posts for connected hotel brand accounts. It supports draft selection, regeneration, account confirmation, publishing status checks, and optional Feishu notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or schedule live social media posts using sensitive workspace and user tokens. <br>
Mitigation: Use least-privilege or dedicated tokens, store uk_* and hp_sk_* values as secrets, and require the agent to show the final draft, destination accounts, platform list, and scheduled time before publishing or scheduling. <br>
Risk: Incorrect credentials or workspace selection can send actions to the wrong HotelPost workspace or fail authorization. <br>
Mitigation: Confirm the AgentAuth user key, HotelPost workspace token, MCP server headers, and connected social accounts before generating or publishing content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tourmind/hotel-social-automator) <br>
- [User Onboarding Guide](references/user-onboarding.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [Conversation Examples](references/conversation-examples.md) <br>
- [Feishu Platform Sending Guide](references/feishu-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool calls, configuration snippets, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include draft content, image handling steps, social account selections, publish or schedule confirmations, and Feishu notification guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
