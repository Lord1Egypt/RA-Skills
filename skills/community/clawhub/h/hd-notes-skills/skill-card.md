## Description: <br>
话袋笔记 helps an agent create, update, and search a user's personal notes through the Huadai notes API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[monkeydb](https://clawhub.ai/user/monkeydb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to save new personal notes, update existing notes, and search prior notes by natural-language requests. It also guides OAuth and local configuration needed before note operations are performed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles OAuth-derived API credentials and a user UUID for private notes. <br>
Mitigation: Keep HUADAI_API_KEY, HUADAI_USER_UUID, OpenClaw configuration, and session logs private; never paste or echo credentials in chat. <br>
Risk: The skill can read and write personal notes through openapi.ihuadai.cn. <br>
Mitigation: Install only if you trust Huadai with notes saved or searched through this integration, and use explicit save, update, or search commands when tighter control is needed. <br>
Risk: In shared or group contexts, a mismatched requester could attempt to access another user's notes. <br>
Mitigation: Use HUADAI_USER_UUID as the access boundary and refuse note access when the requester cannot be matched to the configured owner. <br>


## Reference(s): <br>
- [话袋笔记 API 详细参考](references/api-details.md) <br>
- [配置（必须先完成）](references/config.md) <br>
- [OAuth 授权配置（话袋笔记）](references/oauth.md) <br>
- [新建笔记（Upload）](references/upload.md) <br>
- [更新笔记（Update）](references/update.md) <br>
- [搜索笔记（Search）](references/search.md) <br>
- [话袋官网](https://ihuadai.cn) <br>
- [话袋 OpenAPI Base URL](https://openapi.ihuadai.cn/open/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/monkeydb/hd-notes-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown text with JSON examples, shell commands, and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OAuth-derived credentials and Huadai API responses to report note save, update, and search results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
