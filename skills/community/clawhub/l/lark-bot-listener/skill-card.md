## Description: <br>
Pywayne Lark Bot Listener supports real-time Feishu/Lark message processing over WebSocket with async handlers, message deduplication, temporary attachment download and cleanup, and optional replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build or explain Feishu/Lark bot listeners that receive text, image, file, and post messages, register async handlers, manage temporary attachment files, and send Markdown replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bot may receive Lark/Feishu conversations outside the intended scope if chat membership or app permissions are too broad. <br>
Mitigation: Limit the bot's chat membership and app permissions to approved conversations before deployment. <br>
Risk: Incoming text and downloaded image or file attachments are untrusted input. <br>
Mitigation: Apply environment-appropriate validation, size limits, malware scanning, and temporary-file cleanup. <br>
Risk: Highly sensitive channels may be routed to handlers if the integration is deployed without review. <br>
Mitigation: Avoid routing sensitive conversations unless approved and document the expected data handling path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyendt/lark-bot-listener) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include async handler patterns, credential placeholders, and guidance for handling Lark/Feishu messages and attachments.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
