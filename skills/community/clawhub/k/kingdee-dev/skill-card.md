## Description: <br>
Guides Kingdee Cloud 星空/K3 Cloud and 金蝶云苍穹/Cosmic secondary development, with emphasis on plugin development, BOS modeling, WebAPI integrations, SQL/report work, and deployment operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoqishitou](https://clawhub.ai/user/xiaoqishitou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ERP implementers use this skill to analyze Kingdee ERP customization requests, choose the right extension pattern, and produce implementation guidance for plugins, APIs, reports, database queries, and deployment steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may produce guidance involving sensitive ERP credentials, OAuth tokens, API secrets, or administrator accounts. <br>
Mitigation: Keep production credentials out of prompts, store secrets securely, require HTTPS for login and API traffic, and rotate any exposed credentials. <br>
Risk: Generated ERP administration, WebAPI, SQL, deployment, delete, submit, audit, restore, or session-kill steps can affect production data or availability. <br>
Mitigation: Review high-impact steps before execution, test mutations outside production first, and back up relevant systems before deployment or database changes. <br>
Risk: The artifact includes references to default administrator passwords and operational setup paths. <br>
Mitigation: Change default administrator passwords immediately and restrict administrative access according to the target organization's access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoqishitou/kingdee-dev) <br>
- [SKILL.md](SKILL.md) <br>
- [金蝶云星空插件开发指南](references/xingkong-plugin-dev.md) <br>
- [金蝶云星空插件代码模板库](references/plugin-templates.md) <br>
- [金蝶云星空 BOS IDE 操作手册](references/xingkong-bos-ide.md) <br>
- [金蝶云星空 WebAPI 接口开发](references/xingkong-webapi.md) <br>
- [金蝶云星空数据库参考](references/database-reference.md) <br>
- [金蝶云苍穹二次开发](references/cangqiong-dev.md) <br>
- [金蝶二次开发常见模式 + 社区FAQ](references/common-patterns.md) <br>
- [金蝶云星空部署运维](references/deployment-ops.md) <br>
- [金蝶云星空 WebAPI 接口说明书](https://vip.kingdee.com/knowledge/2569) <br>
- [金蝶云苍穹开发者门户](https://dev.kingdee.com/dev) <br>
- [金蝶云苍穹开发文档](https://demo.kdcloud.com/devdoc/wf) <br>
- [金蝶云星空开放平台](https://open.kingdee.com/k3cloud/open/home) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with C#, Java, Python, SQL, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include environment-specific ERP administration, database, API, and deployment steps that require user review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
