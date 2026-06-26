## Description: <br>
Teach OpenClaw how to work in Feishu (Lark) group chats: recognize senders, behave appropriately in groups and DMs, protect multi-user privacy, and format messages for the platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4ier](https://clawhub.ai/user/4ier) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw operators and developers use this skill when connecting an agent to Feishu group chats or DMs. It provides setup guidance, contact-sync commands, prompt snippets, etiquette rules, and Feishu-specific formatting guidance so the agent can identify senders and avoid leaking private DM context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The contact sync stores Feishu names and open_ids in USER.md, making contact mappings persistent and prompt-visible. <br>
Mitigation: Protect USER.md, exclude it from source control when it contains contact mappings, and limit workspace access to trusted users. <br>
Risk: The sync script reads Feishu app credentials from openclaw.json and requires directory-read access to pull contacts. <br>
Mitigation: Use a least-privilege Feishu app, protect openclaw.json, and rotate credentials if the config file is exposed. <br>
Risk: A weekly cron sync can automatically refresh and retain organization contact data even when automatic refresh is not required. <br>
Mitigation: Run contact sync manually or disable the cron job unless the agent truly needs scheduled contact refreshes. <br>


## Reference(s): <br>
- [OpenClaw Feishu Group Chat release page](https://clawhub.ai/4ier/openclaw-feishu-group-chat) <br>
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu contact users API endpoint](https://open.feishu.cn/open-apis/contact/v3/users/find_by_department?department_id=0&page_size=50) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Feishu contact-sync instructions, USER.md table guidance, AGENTS.md or SOUL.md prompt snippets, and platform formatting rules.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
