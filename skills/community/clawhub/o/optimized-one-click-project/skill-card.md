## Description: <br>
全自动项目生成和启动器 - 生成完整的Spring Boot + Vue3项目，包含前后端完整代码（RBAC+业务实体）、数据库初始化、编译启动、自动浏览器打开。支持完整CRUD（列表、查询、新增、修改、删除、查看）、多条件查询、状态下拉枚举、Redis配置、Swagger文档，使用JSON配置文件自定义参数。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallest-ming](https://clawhub.ai/user/smallest-ming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to generate and start a Spring Boot and Vue 3 CRUD management application from a JSON configuration, including RBAC scaffolding, database initialization, and optional Redis and Swagger setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator can automatically drop and recreate database tables. <br>
Mitigation: Use it only for local development or a disposable sandbox, inspect init.sql first, use a restricted MySQL account, and back up data before running it. <br>
Risk: The generated application includes insecure demo-style authentication and default passwords. <br>
Mitigation: Change or remove the generated default-password authentication before exposing the app to any network. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallest-ming/optimized-one-click-project) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with generated source and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JSON project configuration and local Java, Maven, Node.js, npm, and MySQL-compatible environment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
