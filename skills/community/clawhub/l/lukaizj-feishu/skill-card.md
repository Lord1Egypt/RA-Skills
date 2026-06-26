## Description: <br>
Feishu (Feishu) integration for sending messages, managing groups, and automating workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukaizj](https://clawhub.ai/user/lukaizj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent send Feishu text or card messages, create group chats, list accessible chats, and assist with Feishu workflow automation after app credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Feishu app credentials. <br>
Mitigation: Use a least-privilege Feishu app, store credentials only in environment variables, and treat app secrets and token output as sensitive. <br>
Risk: The skill can send messages and create chats in an external Feishu workspace. <br>
Mitigation: Require explicit user confirmation before sending messages or creating chats, and grant only the Feishu permissions needed for the intended workflow. <br>
Risk: The callable token-retrieval tool can expose token information. <br>
Mitigation: Remove or disable feishu_get_token unless a non-sensitive authentication health check is sufficient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lukaizj/lukaizj-feishu) <br>
- [ClawHub metadata homepage](https://github.com/lukaizj/feishu-integration-skill) <br>
- [Feishu developer console](https://open.feishu.cn/) <br>
- [Feishu Open API endpoint](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance and JSON-like tool result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET; may perform external Feishu messaging and chat-management actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact/claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
