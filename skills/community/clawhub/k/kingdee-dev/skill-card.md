## Description:

金蝶二次开发全栈技能，覆盖金蝶云星空（K3 Cloud）和金蝶云苍穹（Cosmic）的插件开发、BOS 建模、WebAPI、数据库、部署运维、审批流、多组织安全和性能调优 guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoqishitou](https://clawhub.ai/user/xiaoqishitou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and implement Kingdee K3 Cloud and Cosmic custom development work, including plugins, workflow extensions, WebAPI integrations, SQL references, deployment steps, security controls, and performance debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports unsafe credential, authentication, and WebAPI examples.

Mitigation: Treat generated authentication and integration snippets as drafts; require HTTPS, managed secrets, password rotation, least-privilege accounts, and authorization checks before use.

Risk: The security scan flags database restore and production-operations snippets as requiring review.

Mitigation: Test operational changes outside production, take backups, and require an operator review before applying database, deployment, or production maintenance commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoqishitou/skills/kingdee-dev)
- [金蝶云苍穹二次开发](references/cangqiong-dev.md)
- [金蝶二次开发常见模式 + 社区FAQ](references/common-patterns.md)
- [金蝶云星空数据库参考](references/database-reference.md)
- [金蝶云星空部署运维](references/deployment-ops.md)
- [金蝶云星空多组织与安全](references/multi-org-security.md)
- [金蝶云星空性能调优与故障排查](references/performance-debugging.md)
- [金蝶云星空插件代码模板库](references/plugin-templates.md)
- [金蝶云星空审批流插件开发](references/workflow-plugin-dev.md)
- [金蝶云星空 BOS IDE 操作手册](references/xingkong-bos-ide.md)
- [金蝶云星空插件开发](references/xingkong-plugin-dev.md)
- [金蝶云星空 WebAPI 开发](references/xingkong-webapi.md)
- [星空知识地图](https://vip.kingdee.com/article/392699482837824512)
- [星空社区](https://vip.kingdee.com/search?productId=1&productLineId=1)
- [星空环境下载](https://open.kingdee.com/K3Cloud/Open/Products.aspx)
- [WebAPI 接口说明书](https://vip.kingdee.com/knowledge/2569)
- [苍穹开发者门户](https://dev.kingdee.com/dev)
- [苍穹开发文档](https://demo.kdcloud.com/devdoc/wf)
- [星空开放平台](https://open.kingdee.com/k3cloud/open/home)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and structured implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include C#, Java, SQL, JSON, YAML, IIS, Docker, Kubernetes, and Kingdee platform configuration examples.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
