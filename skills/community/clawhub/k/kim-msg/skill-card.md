## Description: <br>
快手 Kim 即时通讯消息发送，支持 Webhook（群聊）和消息号（指定用户）两种方式，内置智能密钥加载和 fallback 机制，适用于通知、告警、日报等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeeGoDamn](https://clawhub.ai/user/LeeGoDamn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to send Kim/Kuaishou IM notifications, alerts, and daily reports to group chats via webhook or to named users through Kim message APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message content and recipient identifiers are transmitted to Kim/Kuaishou systems. <br>
Mitigation: Use only where Kim messaging is intended, and avoid sending secrets, regulated data, or sensitive reports unless organizational policy permits it. <br>
Risk: The skill can load Kim credentials from environment variables or supported local credential files. <br>
Mitigation: Review local Kim/OpenClaw secrets before use, keep credential files access-controlled, and remove stale credentials. <br>


## Reference(s): <br>
- [Kim official website](https://kim.kuaishou.com/) <br>
- [ClawHub release page](https://clawhub.ai/LeeGoDamn/kim-msg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text messages sent through Kim, plus terminal status output and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Kim webhook or app credentials supplied through environment variables or supported local credential files] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
