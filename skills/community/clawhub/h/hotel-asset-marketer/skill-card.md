## Description: <br>
Generate, review, and publish social media content through MCP with AgentAuth and workspace token authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tourmind](https://clawhub.ai/user/tourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams and hotel operators use this skill to generate social media drafts from HotelPost scenarios, review or regenerate copy and images, and publish or schedule approved content to connected social accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive HotelPost workspace and AgentAuth user tokens could grant workspace access if exposed. <br>
Mitigation: Keep tokens private, configure only the required MCP headers, verify the MCP endpoint, and rotate or recreate tokens if exposure is suspected. <br>
Risk: The skill can publish or schedule content on connected social media accounts. <br>
Mitigation: Review generated drafts, selected accounts, publishing time, and post status before publishing or scheduling. <br>
Risk: Feishu notifications may be sent to the wrong recipient if the conversation target is misidentified. <br>
Mitigation: Confirm the Feishu recipient or group identifier before sending cards or images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tourmind/hotel-asset-marketer) <br>
- [HotelPost MCP user onboarding](references/user-onboarding.md) <br>
- [Error handling](references/error-handling.md) <br>
- [Conversation examples](references/conversation-examples.md) <br>
- [Feishu platform sending guide](references/feishu-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with MCP tool calls and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include social media draft copy, image handling commands, and publishing or scheduling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
