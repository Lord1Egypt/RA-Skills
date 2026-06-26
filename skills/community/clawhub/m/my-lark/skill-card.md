## Description: <br>
My Lark helps agents work with Feishu/Lark messages, groups, documents, Drive files, Wiki spaces, calendars, approvals, Bitable records, sheets, boards, and contacts through setup guidance, examples, permissions notes, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longsasasasasa](https://clawhub.ai/user/longsasasasasa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and AI agents use this skill to configure and call Feishu/Lark workspace APIs for messaging, document search and reading, calendar operations, approvals, records, files, and contacts. It is intended for workspace automation where credentials, permissions, and write actions are reviewed before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded app credentials may expose or misuse a Feishu/Lark application secret. <br>
Mitigation: Replace embedded credentials with credentials from the deploying workspace and store secrets in secure storage before use. <br>
Risk: Broad Feishu/Lark business-data actions can read or change production workspace data if granted excessive permissions. <br>
Mitigation: Use least-privilege Feishu permissions and gate write or delete actions with explicit confirmation before production use. <br>
Risk: Token files or API outputs may leak sensitive workspace data through terminals, logs, chats, or agent transcripts. <br>
Mitigation: Avoid printing or pasting token files and review outputs before sharing them outside the trusted workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/longsasasasasa/my-lark) <br>
- [First Use Quick Start](references/start-here.md) <br>
- [Tool Index](references/tools-index.md) <br>
- [Authentication and Permissions](references/auth.md) <br>
- [Error Codes](references/errors.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [Feishu OAuth access token documentation](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/authen-v1/oidc-access-token/create) <br>
- [Feishu Open API base](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and Python helper usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions and command patterns for Feishu/Lark API workflows.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
