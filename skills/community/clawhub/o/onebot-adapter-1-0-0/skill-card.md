## Description: <br>
Connect OpenClaw to OneBot protocol for QQ bot integration. Use when receiving or sending QQ messages via NapCat or other OneBot servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haohaodlam](https://clawhub.ai/user/haohaodlam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to connect OpenClaw agents to OneBot-compatible QQ bot servers, receive private or group messages, and send replies or administrative actions through the OneBot API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose group moderation actions such as kicking or banning users through the OneBot API. <br>
Mitigation: Use a bot account with limited group privileges and review any automation that calls group management endpoints before deployment. <br>
Risk: The WebSocket listener prints full incoming event payloads, which can include real chat content or identifiers. <br>
Mitigation: Disable, redact, or restrict verbose event logging before using the skill with real QQ chats. <br>
Risk: Remote OneBot endpoints without strong authentication can expose bot control over the network. <br>
Mitigation: Prefer local or private OneBot servers, set ONEBOT_TOKEN, and avoid plaintext remote endpoints for production use. <br>


## Reference(s): <br>
- [OneBot Message Handling](references/message-handling.md) <br>
- [ClawHub Release Page](https://clawhub.ai/haohaodlam/onebot-adapter-1-0-0) <br>
- [Publisher Profile](https://clawhub.ai/user/haohaodlam) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OneBot HTTP API calls and WebSocket listener patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
