## Description: <br>
OneBot 11 channel plugin for QQ messaging (NapCat/go-cqhttp), with native OpenClaw integration for private and group chat, opt-in group reactions, block streaming, voice handling, message batching, allowFrom filtering, shared-directory media staging, and authorized text-command passthrough. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xucheng](https://clawhub.ai/user/xucheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to connect OpenClaw agents to QQ through a trusted OneBot 11 provider such as NapCat or go-cqhttp. It helps configure messaging, media delivery, reactions, streaming replies, and authorized text-command handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OneBot endpoint or access token exposure could allow unintended access to QQ messaging routes. <br>
Mitigation: Use a strong access token and keep HTTP/WebSocket endpoints on localhost or a trusted network. <br>
Risk: Overbroad allowFrom settings can authorize more QQ users or groups than intended. <br>
Mitigation: Configure allowFrom narrowly for trusted private users or groups and avoid '*' unless the deployment requires it. <br>
Risk: Using a broad sharedDir can expose unrelated local files during media staging. <br>
Mitigation: Point sharedDir at a dedicated media folder rather than personal document, desktop, or download directories. <br>


## Reference(s): <br>
- [OpenClaw OneBot on ClawHub](https://clawhub.ai/xucheng/openclaw-onebot) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [NapCatQQ](https://github.com/NapNeko/NapCatQQ) <br>
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw plugin configuration, OneBot endpoint settings, allowFrom filters, access-token guidance, and install or verification commands.] <br>

## Skill Version(s): <br>
1.2.15 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
