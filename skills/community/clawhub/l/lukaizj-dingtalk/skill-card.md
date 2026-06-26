## Description: <br>
DingTalk (钉钉) integration - Send messages, create groups, and automate DingTalk workflows <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukaizj](https://clawhub.ai/user/lukaizj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace automation users use this skill to send DingTalk messages, create group chats, list accessible chats, and check DingTalk API access from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act in a real workplace DingTalk account. <br>
Mitigation: Use a dedicated least-privilege DingTalk app and require human confirmation of recipients, message contents, and group membership before taking action. <br>
Risk: The skill requires sensitive DingTalk app credentials. <br>
Mitigation: Store the App Secret only in secure environment variables or secret management and avoid exposing token outputs in prompts or logs. <br>


## Reference(s): <br>
- [DingTalk Open Platform](https://open.dingtalk.com/) <br>
- [DingTalk API Endpoint](https://oapi.dingtalk.com) <br>
- [Skill Homepage](https://github.com/lukaizj/dingtalk-integration-skill) <br>
- [ClawHub Skill Page](https://clawhub.ai/lukaizj/lukaizj-dingtalk) <br>
- [Publisher Profile](https://clawhub.ai/user/lukaizj) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON responses from DingTalk tool calls with text or markdown message content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DingTalk app credentials and optional agent ID supplied through environment variables.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
