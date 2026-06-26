## Description: <br>
Connect OpenClaw to OneBot protocol for QQ bot integration. Use when receiving or sending QQ messages via NapCat or other OneBot servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gu-Heping](https://clawhub.ai/user/Gu-Heping) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to connect OpenClaw agents to QQ through a trusted OneBot or NapCat server, receive private and group events, and send bot responses or moderation actions through the OneBot API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The adapter can send live QQ private and group messages. <br>
Mitigation: Use a dedicated bot account, keep the OneBot token private, and require human approval before sending messages in sensitive contexts. <br>
Risk: The client exposes group moderation actions such as deleting messages, kicking users, banning users, and changing group settings. <br>
Mitigation: Restrict moderation commands to trusted operators and require explicit human approval before executing destructive or administrative actions. <br>
Risk: A reachable OneBot or NapCat endpoint can expose bot control if it is not tightly protected. <br>
Mitigation: Keep endpoints local or otherwise access-controlled, use token authentication, and avoid exposing the service directly to untrusted networks. <br>
Risk: The example WebSocket listener prints incoming event payloads, which may include chat content or user identifiers. <br>
Mitigation: Redact or disable event logging before running the listener in sensitive chats or production-like environments. <br>


## Reference(s): <br>
- [OneBot Message Handling](references/message-handling.md) <br>
- [ClawHub release page](https://clawhub.ai/Gu-Heping/onebot-adapter) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance and reusable Python client/listener patterns for OneBot HTTP and WebSocket integrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
