## Description: <br>
自动为飞书文档添加用户权限，适用于在创建飞书文档后补充访问权限或处理用户反馈的无权限问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sadjjk](https://clawhub.ai/user/sadjjk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw Agent users can use this skill to check Feishu app configuration, resolve document tokens from Feishu links or creation responses, and add a selected user's access to Feishu documents, spreadsheets, folders, files, bitables, and wiki nodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Feishu document permissions and may grant broader access than intended. <br>
Mitigation: Verify the recipient open_id and document before each change, require confirmation for permission updates, and avoid full_access unless it is necessary. <br>
Risk: The skill depends on Feishu app secrets and tenant access tokens. <br>
Mitigation: Keep credentials in protected local settings or a secret store, do not paste App Secret values into chat, and rotate any secret that has been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sadjjk/openclaw-feishu-docs-perm-auto) <br>
- [Feishu permission member batch create documentation](https://open.feishu.cn/document/docs/permission/permission-member/batch_create) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [Feishu Open ID FAQ](https://open.feishu.cn/document/faq/trouble-shooting/how-to-obtain-openid) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Feishu API requests, progress messages, and permission-change results for the agent to review with the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
