## Description: <br>
Pywayne Lark Bot helps agents use Feishu/Lark bot APIs to send rich messages, manage files, query users and groups, and listen for incoming messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to integrate Feishu/Lark bot workflows, including message delivery, Markdown/card formatting, file transfer, user/group lookup, and asynchronous message listeners. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to send, receive, upload, and download Feishu/Lark chat content. <br>
Mitigation: Use a dedicated least-privilege bot app, confirm chat/user IDs and file paths before actions, and keep downloads in a controlled directory. <br>
Risk: Bot app secrets and incoming listener content or attachments can expose sensitive data. <br>
Mitigation: Keep app_secret out of prompts, logs, and shared files, and treat inbound messages and attachments as untrusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyendt/lark-bot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Feishu/Lark message payloads, file paths, chat/user IDs, and listener handler patterns; credentials and attachments require user control.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
