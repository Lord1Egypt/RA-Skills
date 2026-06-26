## Description: <br>
Glow helps agents support a human in finding meaningful connections through private introductions across dating, friendship, activities, and professional networking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robmeadows](https://clawhub.ai/user/robmeadows) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use Glow to register with human authorization, manage profile and preference information, create connection intents, review introductions, exchange messages, manage photos and privacy settings, and configure heartbeat or webhook notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on sensitive social account data, including messages, profile details, photos, introductions, settings, and webhooks. <br>
Mitigation: Use MCP/OAuth when possible, restrict GLOW_API_KEY to agents.talktoglow.com, and require explicit human confirmation before profile updates, photo changes, messages, intro decisions, intent deletion, privacy setting changes, heartbeat polling, or webhook registration. <br>
Risk: Heartbeat polling can repeatedly surface private introductions and messages. <br>
Mitigation: Enable polling only after human approval, store minimal state such as last check time or last seen message ID, and notify the human before acting on new items. <br>


## Reference(s): <br>
- [ClawHub Glow Listing](https://clawhub.ai/robmeadows/glow) <br>
- [Glow Agent API Base](https://agents.talktoglow.com) <br>
- [Glow Skill Documentation](https://agents.talktoglow.com/skill.md) <br>
- [Glow Heartbeat Guide](https://agents.talktoglow.com/heartbeat.md) <br>
- [Glow OpenAPI Specification](https://agents.talktoglow.com/openapi.json) <br>
- [Glow Privacy Policy](https://talktoglow.com/privacy-policy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline JSON and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GLOW_API_KEY for REST use; MCP/OAuth is preferred when available.] <br>

## Skill Version(s): <br>
1.0.3 (source: skill frontmatter, skill.json, OpenAPI info, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
