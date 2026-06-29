## Description: <br>
金蝶二次开发全栈技能，覆盖金蝶云星空（K3 Cloud）和金蝶云苍穹（Cosmic）的插件开发、BOS 建模、WebAPI、工作流、多组织安全、性能调试、数据库参考与部署运维指导。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoqishitou](https://clawhub.ai/user/xiaoqishitou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ERP implementation engineers use this skill to plan and generate guidance, code templates, shell commands, configuration steps, and troubleshooting workflows for Kingdee Cloud Galaxy and Kingdee Cloud Cosmic custom development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production-facing ERP credential and authentication examples may encourage unsafe handling of secrets or insecure transport. <br>
Mitigation: Use HTTPS, keep credentials in environment variables or a secret manager, avoid tokens in URLs, and rotate any default or admin passwords before real use. <br>
Risk: Examples for delete, submit, audit, unaudit, database recovery, and production deployment can change or remove business-critical ERP data. <br>
Mitigation: Require explicit human confirmation, verified backups, and rollback plans before applying destructive or production actions. <br>
Risk: Generated code and configuration guidance may not match the target Kingdee version or local deployment model. <br>
Mitigation: Review, test, and harden examples in a non-production environment before relying on them in ERP work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoqishitou/skills/kingdee-dev) <br>
- [金蝶云星空插件开发指南](references/xingkong-plugin-dev.md) <br>
- [金蝶云星空插件代码模板库](references/plugin-templates.md) <br>
- [金蝶云星空审批流插件开发指南](references/workflow-plugin-dev.md) <br>
- [金蝶云星空多组织与数据权限开发指南](references/multi-org-security.md) <br>
- [金蝶云星空性能优化与调试排错指南](references/performance-debugging.md) <br>
- [金蝶云星空 WebAPI 接口开发](references/xingkong-webapi.md) <br>
- [金蝶云星空 BOS IDE 操作手册](references/xingkong-bos-ide.md) <br>
- [金蝶云星空数据库参考](references/database-reference.md) <br>
- [金蝶云星空部署运维](references/deployment-ops.md) <br>
- [金蝶云苍穹二次开发](references/cangqiong-dev.md) <br>
- [金蝶二次开发常见模式 + 社区FAQ](references/common-patterns.md) <br>
- [星空知识地图](https://vip.kingdee.com/article/392699482837824512) <br>
- [星空开放平台](https://open.kingdee.com/k3cloud/open/home) <br>
- [苍穹开发者门户](https://dev.kingdee.com/dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, tables, command snippets, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed and adapted to the target Kingdee product version and environment before use.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter, _meta.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
